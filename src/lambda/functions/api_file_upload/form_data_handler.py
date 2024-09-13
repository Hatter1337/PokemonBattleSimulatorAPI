import base64
import cgi
import io
import json
import logging
from uuid import uuid4

import boto3

BUCKET_NAME = "YourBucketName"
SUPPORTED_MEDIA_TYPES = {
    "image/png": "png",
    "image/jpeg": "jpeg",
    "image/gif": "gif",
}

# Initialize S3 client
s3_client = boto3.client("s3")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate_request(event: dict):
    """
    Validate the request and return the content type or an error response.

    Args:
        event: The Lambda event object.

    Returns:
        tuple: A tuple containing the content type and an error response.
    """
    headers = event.get("headers", {})
    content_type = headers.get("Content-Type")

    # Validate the request
    if content_type is None:
        return None, {
            "statusCode": 400,
            "body": json.dumps("Content-Type header required"),
        }
    if not event.get("isBase64Encoded", False):
        return None, {
            "statusCode": 400,
            "body": json.dumps("File content is not Base64 encoded"),
        }

    return content_type, None


def get_file_from_request_body(content_type: str, body: str):
    """
    Get the file from the request body.

    Args:
        content_type: The content type of the file.
        body: The base64-encoded body of the request.

    Returns:
        FieldStorage: The file item from the request body.
    """
    try:
        fp = io.BytesIO(base64.b64decode(body))
        environ = {"REQUEST_METHOD": "POST"}
        headers = {
            "content-type": content_type,
        }

        fs = cgi.FieldStorage(fp=fp, environ=environ, headers=headers)
        return fs["file"]
    except Exception as error:
        logger.exception(f"Error decoding file content: {error}")


def lambda_handler(event, context):  # noqa pylint: disable=unused-argument
    # Verify the request
    content_type, error_response = validate_request(event)

    if error_response:
        return error_response

    # Verify the media type and get the file item
    file_item = get_file_from_request_body(content_type=content_type, body=event["body"])

    if file_item is None:
        return {
            "statusCode": 400,
            "body": json.dumps("No file content found in the request"),
        }
    if file_item.type not in SUPPORTED_MEDIA_TYPES:
        return {
            "statusCode": 400,
            "body": json.dumps(f"Unsupported media type: {file_item.type}"),
        }

    # Upload the file to S3
    s3_key = f"{uuid4().hex}.{SUPPORTED_MEDIA_TYPES[file_item.type]}"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=file_item.file.read(),
        ContentType=file_item.type,
    )
    logger.info(f"File uploaded successfully with Key: {s3_key}")

    return {
        "statusCode": 201,
        "body": json.dumps({"key": s3_key}),
    }
