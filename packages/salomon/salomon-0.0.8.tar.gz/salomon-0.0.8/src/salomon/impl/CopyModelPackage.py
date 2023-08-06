import datetime
from dataclasses import dataclass
from typing import List, Dict

import boto3, os, time, tempfile, logging
import docker, docker.utils
from .s3_helper import parse_s3_url


@dataclass()
class FileToCopy:
    src_s3_uri: str
    temp_file: str
    dst_s3_uri: str


@dataclass()
class DockerImageToCopy:
    src_image: str
    src_auth_config: dict   # dict passed to docker pull API
    dst_image: str
    dst_auth_config: dict   # dict passed to docker push API


@dataclass()
class ModelPackage:
    dst_model_package: dict
    files_to_copy: List[FileToCopy]       # source S3 uri, local temp file path, destination S3 uri
    docker_images_to_copy: List[DockerImageToCopy]


def copy_model_package(
        source_arn: str, dst_group_name: str, dst_s3_path: str, dst_ecr: str,
        src_session: boto3.session.Session = None,
        dst_session: boto3.session.Session = None,
        docker_client: docker.client.DockerClient = None,
        src_docker_auths: Dict[str, dict]={}, dst_docker_auth: dict=None
):
    """
    Makes a copy of SageMaker Model Package.

    1. Reads source_arn SageMaker Model Package
    2. Replaces paths for data files with `dst_s3_path`
    3. Replaces docker image URIs with `dst_ecr`
    4. Makes a copy of data files to `dst_s3_path`
    5. Pulls docker images and then pushes to `dst_ecr`
    6. Creates new SageMaker Model Package in current AWS account.

    :param source_arn: source model package ARN.
    :param dst_group_name: target model package group name. It must already exist before calling this function.
    :param dst_s3_path: target S3 path, where model files will be copied to. Automatically there is appended prefix to
        all the files: `dst_group_name/YYYYmmdd-HHMMSS` just not to loose past models. Multiple files with the same
        base name (like two files named 'model.tar.gz' are not supported yet), so files must have unique names,
        otherwise one file would overwrite another.
    :param dst_ecr: target ECR, where images will be copied to. You must successfully authenticate to that repo and have
        push permissions, otherwise you may get strange errors.
    :param src_session: boto3.session.Session, used only in source AWS account. All resources are read from source
        account or environment using this session. It is up to the user to assume-role or get AWS credentials.
    :param dst_session: boto3.session.Session, used only in destination AWS account. All resources are written to target
        account or environment using this session. It is up to the user to assume-role or get AWS credentials.
    :param docker_client: docker.client.DockerClient, used to both pull source and push destination images. It is up
        to the user to invoke docker login() and authenticate to source and target regustry.
    :param src_docker_auths: Dict[str, dict]: key is name of docker registry (hostname, without a path),
        value is a dictionary to be passed to docker API (with username and password fields).
    :param dst_docker_auth: Dict[str, dict]: a dictionary to be passed to docker API (with username and password fields).
    :return: ARN of created model
    """
    logger = logging.getLogger(__name__)

    if src_session is None:
        src_session = boto3.session.Session()
    if dst_session is None:
        dst_session = boto3.session.Session()
    if docker_client is None:
        docker_client = docker.client.from_env()

    with tempfile.TemporaryDirectory() as temp_dir:
        model_package = get_model_package(source_arn, dst_group_name, dst_s3_path, dst_ecr, temp_dir, src_session,
                                          src_docker_auths, dst_docker_auth)
        logger.debug(model_package)

        download_objects(model_package, src_session, docker_client)
        return save_model_package(model_package, dst_session, docker_client)


def get_model_package(source_arn: str, dst_group_name: str, dst_s3_path: str, dst_ecr: str, temp_dir: str,
                      src_session: boto3.session.Session,
                      src_docker_auths: Dict[str, dict]={}, dst_docker_auth: dict=None) -> ModelPackage:
    """

    :param source_arn: source model package ARN.
    :param dst_group_name: target model package group name. It must already exist before calling this function.
    :param dst_s3_path: target S3 path, where model files will be copied to. Automatically there is appended prefix to
        all the files: `dst_group_name/YYYYmmdd-HHMMSS` just not to loose past models. Multiple files with the same
        base name (like two files named 'model.tar.gz' are not supported yet), so files must have unique names,
        otherwise one file would overwrite another.
    :param dst_ecr: target ECR, where images will be copied to. You must successfully authenticate to that repo and have
        push permissions, otherwise you may get strange errors.
    :param temp_dir: temporary directory on local machine. It is required to download source S3 files to.
    :param src_session: boto3.session.Session, used only in source AWS account. All resources are read from source
        account or environment using this session. It is up to the user to assume-role or get AWS credentials.
    :return:
    """
    src_sm = src_session.client('sagemaker')
    src_model_package = src_sm.describe_model_package(ModelPackageName=source_arn)

    return rebuild_model_package(src_model_package, dst_group_name, dst_s3_path, dst_ecr, temp_dir,
                                 src_docker_auths, dst_docker_auth)


def download_objects(model_package: ModelPackage, src_session: boto3.session.Session,
                     docker_client: docker.client.DockerClient):
    """
    Download SageMaker Model Package objects to local machine.

    :param model_package:
    :param src_session:
    :param docker_client:
    :return:
    """
    download_files(model_package.files_to_copy, src_session)
    pull_docker_images(model_package.docker_images_to_copy, docker_client)


def save_model_package(model_package: ModelPackage, dst_session: boto3.session.Session,
                       docker_client: docker.client.DockerClient):
    """
    Save SageMaker Model Package and associated objects to destination AWS Account.

    :param model_package:
    :param dst_session:
    :param docker_client:
    :return:
    """
    logger = logging.getLogger(__name__)

    upload_files(model_package.files_to_copy, dst_session)
    push_docker_images(model_package.docker_images_to_copy, docker_client)

    dst_sm = dst_session.client('sagemaker')
    response = dst_sm.create_model_package(**model_package.dst_model_package)
    print("Model copy completed.")
    logger.debug(response)
    return response.get("ModelPackageArn")


def rebuild_model_package(src_model_package: dict, dst_group_name: str, dst_s3_path: str, dst_ecr: str, temp_dir: str,
                          src_docker_auths: Dict[str, dict], dst_docker_auth: dict) -> ModelPackage:
    dont_copy_keys = [
        'ModelPackageName', 'ModelPackageGroupName',
        'ModelPackageVersion', 'ModelPackageArn', 'CreationTime', 'ModelPackageStatus', 'ModelPackageStatusDetails',
        'CreatedBy', 'LastModifiedTime', 'LastModifiedBy', 'ApprovalDescription', 'ResponseMetadata']

    ts_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    dst_model_package = {}
    for k, v in src_model_package.items():
        if k not in dont_copy_keys:
            dst_model_package[k] = v

    # dst_model_package['ModelPackageName'] = dst_name      # gives error: botocore.exceptions.ClientError: An error occurred (ValidationException) when calling the CreateModelPackage operation: 1 validation errors detected:Environment variable map cannot be specified when using non-versioned ModelPackages
    dst_model_package['ModelPackageGroupName'] = dst_group_name

    files_to_copy = []
    docker_images_to_copy = []
    i=0
    for container in dst_model_package.get("InferenceSpecification").get("Containers"):
        # copy docker image
        p: DockerImageToCopy = prepare_docker_urls(container.get("Image"), dst_ecr, f"{i}-{ts_str}", src_docker_auths, dst_docker_auth)
        docker_images_to_copy.append(p)
        container["Image"] = p.dst_image

        del container["ImageDigest"]

        # copy files
        p: FileToCopy = prepare_file_paths(container.get("ModelDataUrl"), join_uri(dst_s3_path, dst_group_name, ts_str), temp_dir)
        container["ModelDataUrl"] = p.dst_s3_uri
        files_to_copy.append(p)

        if type(container.get("Environment")) is dict:
            for var_name, var_value in container["Environment"].items():
                if var_value.startswith("s3://"):
                    p: FileToCopy = prepare_file_paths(var_value, join_uri(dst_s3_path, dst_group_name, ts_str), temp_dir)
                    container["Environment"][var_name] = p.dst_s3_uri
                    files_to_copy.append(p)
    return ModelPackage(dst_model_package, files_to_copy, docker_images_to_copy)


def prepare_file_paths(src: str, dst_s3_path: str, temp_dir: str) -> FileToCopy:
    filename = os.path.basename(src)
    dst = join_uri(dst_s3_path, filename)
    temp_file = os.path.join(temp_dir, filename)
    return FileToCopy(src, temp_file, dst)


def join_uri(path: str, *elements: str) -> str:
    for filename in elements:
        if path.endswith("/") or path == "":
            path = f"{path}{filename}"
        else:
            path = f"{path}/{filename}"
    return path


def prepare_docker_urls(src_uri: str, dst_ecr: str, tag_suffix: str,
                        src_docker_auths: Dict[str, dict], dst_docker_auth: dict) -> DockerImageToCopy:
    src_repository, src_tag = docker.utils.parse_repository_tag(src_uri)
    src_auth = None
    if "/" in src_repository:
        registry, src_image = src_repository.split("/", maxsplit=1)
        src_auth = src_docker_auths.get(registry)

    tag_infix = src_tag[0:12]
    tag_infix = tag_infix.replace(':', "-")   # for `@sha256:something...` instead of `:tag-name`

    dst_tag = f"img-{tag_infix}-{tag_suffix}"

    return DockerImageToCopy(src_uri, src_auth, f"{dst_ecr}:{dst_tag}", dst_docker_auth)


def download_files(files_to_copy: List[FileToCopy], src_session: boto3.session.Session):
    logger = logging.getLogger(__name__)
    src_s3 = src_session.client('s3')
    for f in files_to_copy:
        src_tuple = parse_s3_url(f.src_s3_uri)
        logger.debug(f"Downloading {f.src_s3_uri} to temp file {f.temp_file}")
        src_s3.download_file(src_tuple[0], src_tuple[1], f.temp_file)


def upload_files(files_to_copy: List[FileToCopy], dst_session: boto3.session.Session):
    logger = logging.getLogger(__name__)
    dst_s3 = dst_session.client('s3')
    for f in files_to_copy:
        dst_tuple = parse_s3_url(f.dst_s3_uri)
        logger.debug(f"Uploading {f.temp_file} to {f.dst_s3_uri}")
        dst_s3.upload_file(f.temp_file, dst_tuple[0], dst_tuple[1])


def pull_docker_images(images_to_copy: List[DockerImageToCopy], docker_client: docker.client.DockerClient):
    logger = logging.getLogger(__name__)
    for img in images_to_copy:
        src_repository, src_tag = docker.utils.parse_repository_tag(img.src_image)
        dst_repository, dst_tag = docker.utils.parse_repository_tag(img.dst_image)

        user_info = f"as user {img.src_auth_config.get('username')}" if img.src_auth_config is not None else "with default credentials"
        logger.debug(f"Pulling image {src_repository}:{src_tag} {user_info}")
        image = docker_client.images.pull(repository=src_repository, tag=src_tag, auth_config=img.src_auth_config)

        logger.debug(f"Tagging image {src_repository}:{src_tag} with {dst_repository}:{dst_tag}")
        image.tag(repository=dst_repository, tag=dst_tag)


def push_docker_images(images_to_copy: List[DockerImageToCopy], docker_client: docker.client.DockerClient):
    logger = logging.getLogger(__name__)
    for img in images_to_copy:
        dst_repository, dst_tag = docker.utils.parse_repository_tag(img.dst_image)
        user_info = f"as user {img.dst_auth_config.get('username')}" if img.dst_auth_config is not None else "with default credentials"
        logger.debug(f"Pushing image {dst_repository}:{dst_tag} {user_info}")

        prev_ts = time.time() - 10
        for line in docker_client.api.push(repository=dst_repository, tag=dst_tag, stream=True, decode=True, auth_config=img.dst_auth_config):
            ts = time.time()
            if ts - prev_ts > 10:
                prev_ts = ts
                logger.info(line)
            else:
                logging.debug(line)
            if 'error' in line.keys():
                raise Exception(f"Can't push to docker registry: {line}")


def list_docker_images_in_model_package(model_package_arn: str, session: boto3.session.Session = boto3.session.Session()):
    sm = session.client('sagemaker')
    src_model_package = sm.describe_model_package(ModelPackageName=model_package_arn)

    return [container.get("Image") for container in src_model_package.get("InferenceSpecification").get("Containers")]

