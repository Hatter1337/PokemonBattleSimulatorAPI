import json
import boto3
import base64
import logging
from uuid import uuid4

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


def decode_file_content(body: str):
    """
    Decode the file content from the request body.

    Args:
        body: The base64-encoded body of the request.

    Returns:
        bytes: The decoded file content.
    """
    try:
        return base64.b64decode(body, validate=True)
    except Exception as error:
        logger.exception(f"Error decoding file content: {error}")
        return None


def lambda_handler(event, context):  # noqa pylint: disable=unused-argument
    # Verify the request
    content_type, error_response = validate_request(event)

    if error_response:
        return error_response

    # Verify the media type
    if content_type not in SUPPORTED_MEDIA_TYPES:
        return {
            "statusCode": 400,
            "body": json.dumps(f"Unsupported media type: {content_type}"),
        }

    # Decode the file content
    file_content = decode_file_content(body=event["body"])

    if file_content is None:
        return {
            "statusCode": 400,
            "body": json.dumps("Error decoding file content."),
        }

    # Upload the file to S3
    s3_key = f"{uuid4().hex}.{SUPPORTED_MEDIA_TYPES[content_type]}"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=file_content,
        ContentType=SUPPORTED_MEDIA_TYPES[content_type],
    )
    logger.info(f"File uploaded successfully with Key: {s3_key}")

    return {
        "statusCode": 201,
        "body": json.dumps({"key": s3_key}),
    }
