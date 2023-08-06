"""Base file of the games without any code dependencies. Necessary
dependencies are loaded at runtime.

This can be safely imported throughout the codebase without worries
of circular dependencies.

"""

import logging
from typing import Any, Dict, List

import yaml

logger = logging.getLogger(__name__)


class GameConfig:
    """Game Config object. Loads the yaml file
    and provides methods for accessing the configuration
    in the yaml file.
    """

    uses_game_accounts_for_sships: bool
    primary_token: str
    contracts: dict[str, Any]
    token_contract_types = [
        "ERC20",
        "ERC721",
        "ETH",
    ]

    def __init__(self, config_filename: str) -> None:
        """
        Initializes a GameConfig object by taking in a config file,
        and then loads the config file into a dictionary

        Args:
          config_filename (str): The path to the config file.
        """
        with open(config_filename, encoding="utf-8") as file_handle:
            game_config_dict = yaml.safe_load(file_handle)

        self.name = game_config_dict["game"]["name"]
        self.game_id = game_config_dict["game"]["game_id"]
        self.uses_game_accounts_for_sships = game_config_dict["game"].get(
            "uses_game_accounts_for_sships", True
        )
        self.primary_token = game_config_dict["game"].get("primary_token", "ETH")
        self.contracts = game_config_dict["contracts"]
        self._actions: List[Dict[str, Any]] = game_config_dict.get("actions", [])

    def token_enum_info(self) -> dict:
        """Returns a dictionary of the token enum info for the tokens in this game"""
        token_enum_info = {}
        for _, contract in self.contracts.items():
            if "short_enum" in contract:
                token_enum_info[contract["short_enum"].lower()] = contract[
                    "short_enum"
                ].upper()
        return token_enum_info

    def all_token_info(self) -> list[dict]:
        """Returns the list of dictionaries, where each
        dict contains information about the token.

        The returned token dictionary entries should contain at least the fields
        in schemas/web_three.TokenInfo.
        """
        token_infos = []

        for slug, contract in self.contracts.items():
            contract = dict(contract)  # make a copy

            # Skip non-token contracts
            if contract["contract_type"] not in self.token_contract_types:
                continue

            # Augment with game name and game id
            contract["game_name"] = self.name
            contract["game_id"] = self.game_id
            contract["contract_slug"] = slug

            token_infos.append(contract)

        return token_infos

    def actions(self) -> List[Dict[str, Any]]:
        """Returns the list of actions that are afforded by the
        game on scholarships

        Returns:
            List[Dict[str, Any]]: List of actions supported by the game
        """
        return self._actions
