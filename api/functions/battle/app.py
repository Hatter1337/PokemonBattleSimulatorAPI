from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.openapi.exceptions import RequestValidationError
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, field_validator

from db_models import BattleModel
from data_validation_ext import ExceptionHandlers
from resource_ext.exceptions import ResourceNotFoundError
from poke_api.client import PokeAPIClient
from poke_cache_utils import get_cache_client, fetch_pokemon_data_with_caching

from battle_simulator import PokemonBattleSimulator


# --------------------------------------------------------------- Application & clients
logger = Logger()
app = APIGatewayRestResolver(enable_validation=True)
exception_handlers = ExceptionHandlers(app=app, logger=logger)
# Initialize client for Cache based on DynamoDB table
cache_cli = get_cache_client(db_type="dynamodb")
# Initialize client for PokeAPI
poke_cli = PokeAPIClient()


# --------------------------------------------------------------- Pydantic validation Models
class Fighters(BaseModel):
    pokemon1: str | int
    pokemon2: str | int

    @field_validator("pokemon1", "pokemon2")
    @classmethod
    def lowercase_if_str(cls, v):
        """
        Ensures the value is converted to lowercase if it is a string.

        Args:
            v (str | int): The value of the pokemon field.

        Returns:
            The same value if it's an int, or the lowercase version if it's a string.

        """
        if isinstance(v, str):
            return v.lower()
        return v


# --------------------------------------------------------------- Validation error handlers
@app.exception_handler(RequestValidationError)
def handle_invalid_params_wrapper(exc: RequestValidationError):
    return exception_handlers.invalid_params(exc)


@app.exception_handler(ResourceNotFoundError)
def handle_not_found_error(exc):
    return exception_handlers.not_found(exc)


# --------------------------------------------------------------- API Resources
@app.post("/api/v1/battle")
def generate_battle(fighters: Fighters):
    fighters_data = {}

    for _, fighter in fighters:
        pokemon_data = fetch_pokemon_data_with_caching(
            cache_cli=cache_cli, poke_cli=poke_cli, pokemon_id=str(fighter)
        )
        pokemon = pokemon_data["name"]
        fighters_data[pokemon] = pokemon_data

    battle_result = PokemonBattleSimulator(fighters_data=fighters_data).result()

    # Creating an instance of the BattleModel with the battle result
    battle_entry = BattleModel(**battle_result)

    # Saving the new battle entry to DynamoDB
    battle_entry.save()

    return Response(
        status_code=200,
        content_type=content_types.APPLICATION_JSON,
        body={"battle_result": battle_result},
    )


@app.get("/api/v1/battle/<battle_id>")
def fetch_battle_data(battle_id: str):
    try:
        battle_data = BattleModel.get(battle_id)

        if not battle_data:
            raise ResourceNotFoundError

        return Response(
            status_code=200,
            content_type=content_types.APPLICATION_JSON,
            body={"battle_result": battle_data.attribute_values},
        )

    except Exception as e:
        logger.exception(f"Fetch battle data, error: {str(e)}")
        return Response(status_code=500)


@app.get("/api/v1/battle/search_by_winner/<name>")
def search_battles_by_winner(name: str):
    opponent_filter: str = app.current_event.get_query_string_value(name="opponent")
    timestamp_filter: str = app.current_event.get_query_string_value(name="timestamp")

    try:
        if opponent_filter:
            # Filtering by 'opponent' name using 'starts with'
            battles = BattleModel.winner_opponent_index.query(
                name, BattleModel.opponent.startswith(opponent_filter)
            )

            if timestamp_filter:
                # Apply second level filtering by 'timestamp'
                battles = [
                    battle for battle in battles if battle.timestamp >= int(timestamp_filter)
                ]
        elif timestamp_filter:
            # Filtering by 'timestamp' using 'greater than or equal to'
            battles = BattleModel.winner_timestamp_index.query(
                name, BattleModel.timestamp >= int(timestamp_filter)
            )
        else:
            # Querying only with the 'winner' name
            battles = BattleModel.winner_timestamp_index.query(name)

        battles_data = [battle.attribute_values for battle in battles]

        return Response(
            status_code=200,
            content_type=content_types.APPLICATION_JSON,
            body={"battles": battles_data},
        )

    except Exception as e:
        logger.exception(f"Search battle battle data, error: {str(e)}")
        return Response(status_code=500)


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
