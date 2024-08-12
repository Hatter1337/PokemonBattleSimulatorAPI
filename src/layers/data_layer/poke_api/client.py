import random
import logging
from functools import cached_property

import requests
from requests import Session
from requests.adapters import HTTPAdapter, Retry


class PokeAPIClient:
    """Client for Poke API."""

    base_url = "https://pokeapi.co/api/v2/pokemon/"
    mirror_url = None

    def __init__(self, jitter_type="balanced", total_retries=3, backoff_factor=0.5):
        self.jitter_type = jitter_type
        self.total_retries = total_retries
        self.backoff_factor = backoff_factor
        # Configure logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    @property
    def jitter_coefficient(self) -> float:
        """
        Calculate the jitter coefficient based on the jitter type.

        Returns:
            float: The jitter coefficient.
        """
        settings = {
            "none": (1, 1),
            "balanced": (0.75, 1.25),
            "aggressive": (0.5, 2.0),
            "conservative": (0.9, 1.1),
        }
        jitter_coefficient_range = settings.get(self.jitter_type, (0.75, 1.25))
        return random.uniform(*jitter_coefficient_range)

    @cached_property
    def session(self) -> Session:
        """
        Creates a persistent requests session with a retry policy for API requests.

        Returns:
            Session: A configured requests' session.
        """
        retry_strategy = Retry(
            total=self.total_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.verify = False
        return session

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
        return {
            "id": pokemon_data["id"],
            "name": pokemon_data["name"],
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]},
            "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
            "types": [type_["type"]["name"] for type_ in pokemon_data["types"]],
            "pokemon_image": pokemon_data["sprites"]["front_default"],
        }

    def fetch_pokemon_data(self, pokemon_id, battle_data=True):
        """
        Fetches data for a given Pokemon by its ID or name from PokeAPI.

        Args:
            pokemon_id (str or int): The Pokemon ID or name.
            battle_data (bool): Whether to extract battle data from the full Pokemon data.

        Returns:
            dict: Pokemon data relevant for battles, including name and stats, or
                  None if the data could not be fetched.
        """
        url = f"{self.mirror_url or self.base_url}{pokemon_id}"

        try:
            response = self.session.get(url)

            if response.status_code == 200:
                pokemon_data = response.json()
                return self.extract_battle_data(pokemon_data=pokemon_data) if battle_data else pokemon_data
            elif response.status_code == 404:
                return None
            else:
                self.logger.error(f"HTTP Error: {response.status_code}.")
        except requests.exceptions.RequestException as e:
            self.logger.exception(f"Request failed: {str(e)}")
            return None
