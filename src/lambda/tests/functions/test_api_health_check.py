import os
import sys
import json

import pytest


@pytest.fixture(scope="module")
def health_check_handler(import_module_from_path):
    # Define the paths to your handler.py files and other modules
    service_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    api_users_function_path = os.path.join(service_root, "src", "lambda", "functions", "api_health_check")

    # Add the directory containing the handler.py to sys.path
    sys.path.append(api_users_function_path)

    # Import the handler module
    handler_module_path = os.path.join(api_users_function_path, "handler.py")
    return import_module_from_path("health_check_handler", handler_module_path)


class TestApiHealthCheck:
    """Tests for the api_health_check Lambda function."""

    def test_check_health(self, health_check_handler, lambda_context):
        # Simulate a minimal API Get request event with POST request
        minimal_event = {
            "path": "/v1/health_check",
            "httpMethod": "GET",
        }

        # Call the lambda_handler with the simulated event and mock context
        response = health_check_handler.lambda_handler(event=minimal_event, context=lambda_context)

        # Assert that the Lambda function returns a status code of 200, indicating success
        assert response["statusCode"] == 200

        # Parse the response body from JSON string to a Python dictionary
        body = json.loads(response["body"])

        # Assert that the response body matches the expected response
        expected_response_body = {"status": "healthy"}
        assert body == expected_response_body
