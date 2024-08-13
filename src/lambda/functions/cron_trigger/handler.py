import json
import logging
from datetime import datetime, UTC

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    now = datetime.now(UTC).strftime("%m/%d/%Y, %H:%M:%S")
    logger.info(f"Event received at {now}")
    return {"statusCode": 200, "body": json.dumps("Event processed.")}
