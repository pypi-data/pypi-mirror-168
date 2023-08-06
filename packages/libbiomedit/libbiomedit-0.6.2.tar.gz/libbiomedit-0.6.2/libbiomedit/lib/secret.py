from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class Secret(Generic[T]):
    """A class to mark arguments as sensitive"""

    def __init__(self, val: T):
        self._val = val

    def __repr__(self) -> str:
        return "***"

    def __format__(self, format_spec: str) -> str:
        return str.__format__("***", format_spec)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Secret) and other.reveal() == self._val

    def reveal(self) -> T:
        return self._val


def reveal(secret: Optional[Secret[T]]) -> Optional[T]:
    return None if secret is None else secret.reveal()
