from typing import TypeVar


class IrrecognizableValue(BaseException):
    """
    Exception raised when value doesn't match any known pattern
    """

    def __init__(self, val: str = "") -> None:
        if val:
            super().__init__(f"Value {val} doesn't match any known pattern")


T = TypeVar("T")
