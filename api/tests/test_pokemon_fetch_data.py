import json
from dataclasses import dataclass

import pytest

from api.functions.pokemon import fetch_data


@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:eu-west-1:123456789012:function:test"
        aws_request_id: str = "da658bd3-2d6f-4e7b-8ec2-937234644fdc"

    return LambdaContext()


def test_lambda_handler(lambda_context):
    minimal_event = {
        "path": "/api/v1/pokemon/squirtle",
        "httpMethod": "GET",
        "requestContext": {"requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"},  # correlation ID
    }

    ret = fetch_data.lambda_handler(minimal_event, lambda_context)

    assert ret["statusCode"] == 200
    response = json.loads(ret["body"])

    assert "pokemon_data" in response
    assert all(field in response["pokemon_data"] for field in ("id", "name", "stats"))