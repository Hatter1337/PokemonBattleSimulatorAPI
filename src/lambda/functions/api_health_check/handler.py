import json


def lambda_handler(event, context):
    response_body = {"status": "healthy"}
    return {"statusCode": 200, "body": json.dumps(response_body)}
