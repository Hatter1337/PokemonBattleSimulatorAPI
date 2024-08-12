import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    for record in event["Records"]:
        s3_object_key = record["s3"]["object"]["key"]
        logger.info(f"New object uploaded: {s3_object_key}")

    return {"statusCode": 200, "body": json.dumps("Event processed.")}
