import json

from poke_api.client import PokeAPIClient


def lambda_handler(event, context):
    # Extract the pokemon_id from the path parameters
    pokemon_id = event["pathParameters"]["pokemon_id"]

    # Initialize the PokeAPIClient
    poke_cli = PokeAPIClient()

    # Fetch the Pokemon data using the extracted pokemon_id
    pokemon_data = poke_cli.fetch_pokemon_data(pokemon_id=pokemon_id, battle_data=False)

    # Return the response
    if pokemon_data:
        return {"statusCode": 200, "body": json.dumps(pokemon_data)}
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": f"Pokemon with ID {pokemon_id} not found"}),
        }
