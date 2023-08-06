# Salomon
Sage mAker modeL cOpy froM One account to aNother

Solves everlasting issues with Amazon SageMaker:
1. Make copy of a SageMaker model from one account to another (or from one environment to another)
2. Freeze SageMaker model, so that model used for SageMaker endpoints is immutable and safe from incidental modifications by data scientists
3. Single-command operation for model copy (fills gaps present in Terraform, CloudFormation, etc.) 

(currently works only with SageMaker Model Package. TODO: add SageMaker Model support.)

## Installation

```shell
pip install salomon
```

## Make a copy of SageMaker Model Package

Use `copy_model_package()` function. It makes a copy of SageMaker Model Package.
    
    1. Reads source_arn SageMaker Model Package
    2. Replaces paths for data files with `dst_s3_path`
    3. Replaces docker image URIs with `dst_ecr`
    4. Makes a copy of data files to `dst_s3_path`
    5. Pulls docker images and then pushes to `dst_ecr`
    6. Creates new SageMaker Model Package in current AWS account.

Example:

1. Prepare IAM role that can access both source and destination SageMaker resources, ECRs and S3 files
2. Authenticate to all source docker registries, for example:
```shell
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 492215442770.dkr.ecr.eu-central-1.amazonaws.com
# all other ECRs ...
```
3. Execute below code with IAM role created in point 1.

```python
from salomon import copy_model_package

copy_model_package(
    source_arn="arn:aws:sagemaker:eu-central-1:1111111111:model-package/source-model-package/1",
    dst_group_name="copy-of-model-package",
    dst_s3_path="s3://bucket-in-22222222222/copy-of-model-package",
    dst_ecr="22222222222.dkr.ecr.eu-central-1.amazonaws.com/copy-of-model-package"   
)
```
