"""Models for GameBase"""
# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods

from typing import List, Optional


class UserWallet:
    public_address: str = ""


class GameAccount:
    public_address: str


class Scholarship:
    game_nfts: List = []
    game_account: Optional[GameAccount]
