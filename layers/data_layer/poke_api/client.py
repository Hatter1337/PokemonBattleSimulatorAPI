import time
import random
import logging
from functools import cached_property

import requests


class PokeAPIClient:
    """
    Client for Poke API.

    """

    def __init__(self, base_url="https://pokeapi.co/api/v2/pokemon/", logger=None):
        self.base_url = base_url
        self._logger = logger

    @cached_property
    def logger(self):
        if self._logger:
            return self._logger

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger

    def fetch_pokemon_data(self, pokemon_id, retry_delays=None, jitter_type="default"):
        """
        Fetches data for a given Pokemon by its ID or name from PokeAPI,
        implementing exponential backoff with configurable jitter in case of API request failures.

        Args:
            pokemon_id (str or int): The Pokemon ID or name.
            retry_delays (list of int): A list of delays (in seconds) between retry attempts.
                Default is [1, 3, 8, 21, 55] for retries after 1s, 3s, 8s, 21s, and ~1min.
            jitter_type (str or None): Type of jitter to apply on retry delays.
               Can be "balanced" (default), "aggressive", "conservative", or None for no jitter.

        Returns:
            dict: Pokemon data relevant for battles, including name and stats, or
                  None if the data could not be fetched.

        """
        url = f"{self.base_url}{pokemon_id}/"

        if retry_delays is None:
            retry_delays = [1, 3, 8, 21, 55]

        jitter_ranges = {
            "balanced": (0.75, 1.25),
            "aggressive": (0.5, 2.0),
            "conservative": (0.9, 1.1),
            None: (1, 1),  # No jitter
        }
        jitter_coefficient_range = jitter_ranges.get(jitter_type, (0.75, 1.25))

        for attempt, base_delay in enumerate(retry_delays):
            try:
                response = requests.get(url)

                if response.status_code == 200:
                    pokemon_data = response.json()
                    return self.extract_battle_data(pokemon_data=pokemon_data)
                elif response.status_code == 404:
                    return None
                else:
                    self.logger.error(f"HTTP Error: {response.status_code}. Retrying...")
            except requests.exceptions.RequestException as e:
                self.logger.exception(f"Request failed: {str(e)}")

            # Calculate delay with jitter
            delay = round(base_delay * random.uniform(*jitter_coefficient_range))
            self.logger.info(f"Waiting {delay}s before retry #{attempt + 1}")
            time.sleep(delay)

        self.logger.error(f"Max attempts reached. Failed to fetch Pokemon '{pokemon_id}' data.")
        return None

    @staticmethod
    def extract_battle_data(pokemon_data):
        """
        Extracts relevant battle data from the full Pokemon data.

        This function extracts and organizes important information about a Pokemon
        that can be useful for battles. This includes the Pokemon's name, stats,
        abilities, types, and a default sprite image.

        Args:
            pokemon_data (dict): Full Pokemon data retrieved from the PokeAPI.

        Returns:
            dict: A dictionary containing structured data relevant to Pokemon battles,
                  including the name, stats, abilities, types, and a default sprite image.

        """
        battle_data = {
            "id": pokemon_data["id"],
            "name": pokemon_data["name"],
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]},
            "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
            "types": [type_["type"]["name"] for type_ in pokemon_data["types"]],
            "pokemon_image": pokemon_data["sprites"]["front_default"],
        }
        return battle_data
