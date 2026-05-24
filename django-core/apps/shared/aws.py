"""
Thin boto3 client factory. Reads AWS_ENDPOINT_URL from env so the same
code works against LocalStack (dev) and real AWS (prod).
"""
import boto3
from decouple import config


def _boto_kwargs() -> dict:
    endpoint = config("AWS_ENDPOINT_URL", default="")
    kwargs: dict = {
        "region_name": config("AWS_DEFAULT_REGION", default="eu-central-1"),
        "aws_access_key_id": config("AWS_ACCESS_KEY_ID", default="test"),
        "aws_secret_access_key": config("AWS_SECRET_ACCESS_KEY", default="test"),
    }
    if endpoint:
        kwargs["endpoint_url"] = endpoint
    return kwargs


def sqs_client():
    return boto3.client("sqs", **_boto_kwargs())


def sns_client():
    return boto3.client("sns", **_boto_kwargs())


def s3_client():
    return boto3.client("s3", **_boto_kwargs())


def dynamodb_resource():
    return boto3.resource("dynamodb", **_boto_kwargs())
