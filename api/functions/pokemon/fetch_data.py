from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.openapi.exceptions import RequestValidationError
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

from data_validation_ext import ExceptionHandlers
from resource_ext.exceptions import ResourceNotFoundError
from poke_api.client import PokeAPIClient
from poke_cache_utils import get_cache_client, fetch_pokemon_data_with_caching


# --------------------------------------------------------------- Application & clients
logger = Logger()
app = APIGatewayRestResolver()
exception_handlers = ExceptionHandlers(app=app, logger=logger)
# Initialize client for Cache based on DynamoDB table
cache_cli = get_cache_client(db_type="dynamodb")
# Initialize client for PokeAPI
poke_cli = PokeAPIClient()


# --------------------------------------------------------------- Validation error handlers
@app.exception_handler(RequestValidationError)
def handle_invalid_params_wrapper(exc: RequestValidationError):
    return exception_handlers.invalid_params(exc)


@app.exception_handler(ResourceNotFoundError)
def handle_not_found_error(exc):
    return exception_handlers.not_found(exc)


# --------------------------------------------------------------- API Resources
@app.get("/api/v1/pokemon/<pokemon_id>")
def fetch_pokemon_data(pokemon_id: str | int):
    pokemon_data = fetch_pokemon_data_with_caching(
        cache_cli=cache_cli, poke_cli=poke_cli, pokemon_id=str(pokemon_id)
    )
    logger.info(f"{pokemon_data=}")

    return Response(
        status_code=200,
        content_type=content_types.APPLICATION_JSON,
        body={"pokemon_data": pokemon_data},
    )


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
