from cache.dynamodb import DynamoDBCacheClient

# from cache.redis import RedisCacheClient
from resource_ext.exceptions import ResourceNotFoundError


def get_cache_client(db_type):
    """
    Factory method for creating cache client instances based on the database type.

    Args:
        db_type (str): The type of database for which to create a cache client.
            Supported databases: 'dynamodb' and 'redis'.

    Returns:
        An instance of a cache client, either DynamoDBCacheClient or RedisCacheClient,
        configured for the specified database type.

    Raises:
        NotImplemented: If a cache client for the specified database type is not implemented.

    """
    if db_type == "dynamodb":
        return DynamoDBCacheClient(table_name="pokemon")
    elif db_type == "redis":
        raise NotImplemented(f"Cache client not implemented for {db_type}")
        # return RedisCacheClient(
        #     startup_nodes=[{"host": "{RedisHost}", "port": "6379"}], password="{RedisPassword}"
        # )
    else:
        raise NotImplemented(f"Cache client not implemented for {db_type}")


def fetch_pokemon_data_with_caching(cache_cli, poke_cli, pokemon_id):
    """
    Retrieves Pokémon data, prioritizing cache with a lazy loading strategy. If data is not found
    in the cache, it fetches from the primary source and updates the cache with a TTL.

    Args:
        cache_cli: The cache client instance to use for attempting to retrieve Pokémon data.
        poke_cli: The Pokémon client instance used for fetching data directly if not in cache.
        pokemon_id (str): The unique identifier for the Pokémon to retrieve.

    Returns:
        The Pokémon data either from the cache or directly fetched.

    Raises:
        ResourceNotFoundError: If Pokémon data cannot be found in both cache and primary source.

    """
    pokemon_data = cache_cli.get(key=pokemon_id)  # Attempt to get pokemon data from cache

    if pokemon_data is None:  # If not in cache, fetch from primary source and cache the result
        pokemon_data = poke_cli.fetch_pokemon_data(pokemon_id=pokemon_id)

        if pokemon_data:
            cache_cli.set(key=pokemon_id, value=pokemon_data, ttl=3600)  # Cache with TTL
        else:
            raise ResourceNotFoundError(f"Pokemon data not found for ID: {pokemon_id}")

    return pokemon_data
