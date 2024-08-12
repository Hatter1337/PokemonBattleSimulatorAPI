import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    for record in event["Records"]:
        event_name = record["eventName"]
        dynamodb_record = record["dynamodb"]
        logger.info(f"Event name: {event_name}")
        logger.info(f"DynamoDB Record: {json.dumps(dynamodb_record)}")

    return {"statusCode": 200, "body": json.dumps("Event processed.")}
