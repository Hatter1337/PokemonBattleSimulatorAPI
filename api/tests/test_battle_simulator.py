import os
import sys

import pytest

# Define the project root as a relative path from this test file
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Path to the directory containing the PokemonBattleSimulator class
my_function_path = os.path.join(project_root, "api", "functions", "battle")
sys.path.insert(0, my_function_path)
from battle_simulator import PokemonBattleSimulator, PokemonBattleSimulatorException  # noqa

# Adjusted example fighters data structure for tests
fighters_data_example = {
    # Updated to use IDs for keys as per the simplified method's expected input
    "1": {
        "name": "Bulbasaur",
        "stats": {
            "attack": 49,
            "defense": 49,
            "speed": 45,
            "special-attack": 65,
            "special-defense": 65,
        },
        "abilities": ["overgrow", "chlorophyll"],
        "types": ["grass"],
        "pokemon_image": "https://example.com/bulbasaur.png",
    },
    "2": {
        "name": "Charmander",
        "stats": {
            "attack": 52,
            "defense": 43,
            "speed": 65,
            "special-attack": 60,
            "special-defense": 50,
        },
        "abilities": ["blaze", "solar-power"],
        "types": ["fire"],
        "pokemon_image": "https://example.com/charmander.png",
    },
    "3": {
        "name": "Squirtle",
        "stats": {
            "attack": 48,
            "defense": 65,
            "speed": 43,
            "special-attack": 50,
            "special-defense": 64,
        },
        "abilities": ["torrent", "rain-dish"],
        "types": ["water"],
        "pokemon_image": "https://example.com/squirtle.png",
    },
}


@pytest.mark.parametrize(
    "fighters_data, expected_winner_id",
    [
        # Test scenarios that involve the randomness condition.
        ({"1": fighters_data_example["1"], "2": fighters_data_example["2"]}, "1"),
        ({"2": fighters_data_example["2"], "3": fighters_data_example["3"]}, "2"),
    ],
)
def test_battle_result_with_randomness(mocker, fighters_data, expected_winner_id):
    """
    Tests that the simulator correctly identifies the winner,
    applying randomness when fighters' stats are close.

    """
    mocker.patch("random.choice", return_value=expected_winner_id)
    simulator = PokemonBattleSimulator(fighters_data)
    result = simulator.result()

    assert (
        result["winner"] == expected_winner_id
    ), "The determined winner does not match the expected outcome."


def test_incorrect_number_of_fighters():
    """
    Verifies that the simulator raises an exception
        when initialized with an incorrect number of fighters.

    """
    fighters_data = {"1": {"name": "Pikachu", "stats": {"attack": 55, "defense": 40, "speed": 90}}}

    with pytest.raises(PokemonBattleSimulatorException) as exc_info:
        _ = PokemonBattleSimulator(fighters_data)

    assert (
        str(exc_info.value) == "Exactly two fighters are required."
    ), "Expected an exception for incorrect number of fighters."
