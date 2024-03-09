import time
import random
from uuid import uuid4


class PokemonBattleSimulatorException(Exception):
    """Exception for the PokemonBattleSimulator."""


class PokemonBattleSimulator:
    """
    A class to simulate a Pokemon battle between two fighters.

    Attributes:
        fighters_data (dict): A dictionary with pokemon ID/name as keys
            and their battle data as values.

    """

    def __init__(self, fighters_data):
        """
        Initializes the simulator with fighters data.

        Args:
            fighters_data (dict): A dictionary containing the data of the two pokemons.

        """
        if len(fighters_data) != 2:
            raise PokemonBattleSimulatorException("Exactly two fighters are required.")

        self.fighters_data = fighters_data

    def result(self):
        """
        Determines the battle's outcome.

        Returns:
            dict: Battle result, including winner, opponent, and their stats.

        """
        total_stats = {
            pokemon_id: sum(fighter["stats"].values())
            for pokemon_id, fighter in self.fighters_data.items()
        }
        pre_winner_id, pre_opponent_id = sorted(total_stats, key=total_stats.get, reverse=True)

        # Determine if randomness applies (the weakest has >= 80% of the stats of the stronger)
        if total_stats[pre_opponent_id] >= total_stats[pre_winner_id] * 0.8:
            # The weakest has a chance to win
            winner = random.choice([pre_winner_id, pre_opponent_id])
            opponent = pre_winner_id if pre_winner_id != winner else pre_opponent_id
        else:
            winner, opponent = pre_winner_id, pre_opponent_id

        return {
            "id": uuid4().hex,
            "winner": winner,
            "opponent": opponent,
            "timestamp": int(time.time()),
            "winner_total_stats": total_stats[winner],
            "opponent_total_stats": total_stats[opponent],
        }
