from io import BytesIO

import boto3

from app.core.data.file_stream import FileStream
from app.core.utils.file_util import get_name

s3 = boto3.client("s3")


def download_file(bucket, key, filename):
    s3.download_file(bucket, key, filename)


def stream_response(bucket, key, download=False) -> FileStream:
    obj = s3.get_object(Bucket=bucket, Key=key)
    content_type = obj["ContentType"]
    headers = {
        "Content-Type": content_type,
        "Content-Length": str(obj["ContentLength"]),
        "ETag": obj["ETag"]
    }

    if download:
        name = get_name(key)
        headers["Content-Disposition"] = f"attachment; filename={name}"

    return FileStream(obj["Body"], headers, content_type)


def upload_file(file: BytesIO, content_type, bucket, key):
    extra_args = {
        "ContentType": content_type
    }

    s3.upload_fileobj(file, bucket, key, ExtraArgs=extra_args)


def delete_file(bucket, key):
    s3.delete_object(Bucket=bucket, Key=key)
