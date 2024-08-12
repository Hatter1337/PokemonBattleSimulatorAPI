from aws_lambda_powertools.event_handler import Response, content_types

from data_validation_ext.helper import validation_error_description


class ExceptionHandlers:
    """
    A class to handle common exceptions for AWS Lambda functions using AWS Lambda Powertools.

    Attributes:
        app (LambdaPowertoolsApp): An instance of the LambdaPowertoolsApp.
        logger (Logger): An instance of the Powertools Logger.
    """

    def __init__(self, app, logger):
        self.app = app
        self.logger = logger

    def invalid_params(self, exc):
        """
        Handles RequestValidationError exceptions
            by logging the error and returning a custom Response.

        Args:
            exc (RequestValidationError): The exception object.

        Returns:
            Response: A custom response with a status code of 400, indicating a bad request.
        """
        error_description = validation_error_description(exc)
        self.logger.error(
            f"Data validation error: {error_description}",
            extra={
                "path": self.app.current_event.path,
                "query_strings": self.app.current_event.query_string_parameters,
            },
        )

        return Response(
            status_code=400,
            content_type=content_types.APPLICATION_JSON,
            body={"error": "InvalidRequestParams", "description": error_description},
        )

    @staticmethod
    def not_found(exc):
        """
        Handles resource not found exceptions by returning a custom Response.

        Args:
            exc (Exception): The exception object.

        Returns:
            Response: A custom response with a status code of 404,
                indicating that the resource was not found.
        """
        return Response(
            status_code=404,
            content_type=content_types.APPLICATION_JSON,
            body={"error": "ResourceNotFound"},
        )
