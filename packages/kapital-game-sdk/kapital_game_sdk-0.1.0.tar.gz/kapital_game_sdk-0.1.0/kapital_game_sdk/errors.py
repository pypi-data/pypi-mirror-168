"""Module with errors"""


class ServiceInputError(ValueError):
    """Service error where inputs are invalid."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class ServiceExecutionError(Exception):
    """Service error where there's an error during execution"""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
