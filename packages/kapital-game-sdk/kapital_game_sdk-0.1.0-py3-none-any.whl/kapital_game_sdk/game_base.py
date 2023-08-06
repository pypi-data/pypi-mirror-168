"""Module with GameImplementationBase"""
# pylint: disable=unused-argument,missing-function-docstring,too-few-public-methods

import logging
from typing import Any, Dict, List, Union

from .errors import ServiceInputError
from .game_config import GameConfig
from .models import GameAccount, Scholarship, UserWallet

logger = logging.getLogger(__name__)


class Contract:
    """Contract"""

    zero_address = "0x0000000000000000000000000000000000000000"

    def __init__(self) -> None:
        pass

    def execute(
        self, operation: str, from_address: str | None, contract_args: Dict[str, Any]
    ) -> Dict:
        """Executes a method on the contract

        TODO: clarify error behavior. If this does not 100% succeed, should an exception be raised?
        """
        return {}


class GameImplementationBase:
    """GameImplementationBase class that should be implemented
    to integrate a game with the SDK.

    The base comes with a number of methods, each of which can be overridden
    by the subclass.

    The init function should:
    - Set self.game_name to the game's name

    No methods are required to be overwritten
    """

    game_name: str = ""
    game_config: GameConfig
    contracts: Dict[str, Contract]

    def __init__(self) -> None:
        self.contracts = {}

    def initialize(self) -> None:
        pass

    def get_contract(self, slug: str) -> Contract:
        slug = slug.lower()
        return self.contracts[slug]

    def rent_scholarship(
        self, scholarship: Scholarship, user_wallet: UserWallet
    ) -> Union[Dict, List[Dict]]:
        return {}

    def revoke_scholarship(
        self, scholarship: Scholarship, user_wallet: UserWallet
    ) -> Union[Dict, List[Dict]]:
        return {}

    def batch_nft_transfer(
        self,
        from_address: str,
        to_address: str,
        token_ids: List[int],
        token_symbol: str,
    ) -> Dict:
        return {}

    def retrieve_login_info(self, game_account: GameAccount) -> Dict:
        return {}

    def get_actions(self) -> List[Dict[str, Any]]:
        """Returns the list of actions that can be performed in the game."""
        return self.game_config.actions()

    def do_action(
        self, action_name: str, inputs: Dict[str, Any], sship: Scholarship
    ) -> Dict:
        """
        Takes an action_name and inputs and executes the action for
        the scholarship.

        This implementation does not do any validation of the inputs.

        Args:
          action_name (str): The name of the action to execute.
          inputs (Dict[str, Any]): The inputs to the action.
          sship (Scholarship): Scholarship

        Returns:
          The result of the execution of the operation on the contract.
        """
        logger.info(
            "Executing action {action_name} with inputs {inputs} "
            "for scholarship {sship.id}"
        )

        if not sship.game_account:
            raise ServiceInputError("Scholarship must have a game account")

        # Find the action configuration
        action = None
        for iter_action in self.get_actions():
            if iter_action["action"] == action_name:
                action = dict(iter_action)
                break

        if not action:
            logger.warning("Action not found for game %s: %s", self.game_name, action)
            raise ServiceInputError("Invalid action.")

        # Prepare inputs for the execution
        contract = action["contract"]
        operation = action["operation"]
        contract = self.get_contract(contract)
        addr: str = sship.game_account.public_address

        return contract.execute(operation, addr, inputs)
