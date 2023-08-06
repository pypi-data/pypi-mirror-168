from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re
from typing import List, Callable, Optional, Dict, Any

from .lib.deserialize import deserialize, serialize

METADATA_FILE = "metadata.json"
METADATA_FILE_SIG = "metadata.json.sig"


class ValidatedStr(str):
    validator: Callable[[str], str] = str

    def __new__(cls, val: str) -> "ValidatedStr":
        return super().__new__(cls, cls.validator(val))


def hex_str(
    min_bits: int,
    max_bits: Optional[int] = None,
    normalize: Callable[[str], str] = lambda x: x,
) -> Callable[[str], str]:
    regex = r"[0-9A-Fa-f]{" + str(min_bits // 4)
    if max_bits is not None:
        regex += r"," + str(max_bits // 4)
    regex += r"}"

    def new(s: str) -> str:
        if not re.fullmatch(regex, s):
            rng = str(min_bits)
            if max_bits:
                rng += f"-{max_bits}"
            raise ValueError(f"Invalid hex string (length: {rng}): {s}")
        return normalize(s)

    return new


def alnum_str(
    min_length: int, max_length: int, allow_dots: bool = False
) -> Callable[[str], str]:
    """Generate a 'type definition' function that will check that a string is
    composed only of alphanumeric characters, dashes and underscores, and has
    a length between min_length and max_length.

    :param min_length: minimum length of string type.
    :param max_length: maximum length of string type.
    :param allow_dots: if True, dots are also allowed in the string type.
    :return: 'type definition' function.
    :raises ValueError:
    """
    regexp = (
        r"[0-9A-Za-z"
        + (r"." if allow_dots else r"")
        + r"_-]{"
        + str(min_length)
        + r","
        + str(max_length)
        + r"}"
    )

    def _alnum_str(string_to_check: str) -> str:
        if not re.fullmatch(regexp, string_to_check):
            raise ValueError(
                f"Invalid alphanumeric string: '{string_to_check}'. "
                f"This string can only contain alphanumeric characters, "
                f"{'dots, ' if allow_dots else ''}dashes and underscores. "
                f"It must have a length between {min_length} and "
                f"{max_length} characters."
            )
        return string_to_check

    return _alnum_str


class HexStr1024(ValidatedStr):
    validator = hex_str(128, 1024)


class HexStr256(ValidatedStr):
    validator = hex_str(256, normalize=str.lower)


DATE_FMT = "%Y-%m-%dT%H:%M:%S%z"


class Purpose(Enum):
    PRODUCTION = "PRODUCTION"
    TEST = "TEST"


@dataclass(frozen=True)
class MetaData:
    sender: HexStr1024
    recipients: List[HexStr1024]
    checksum: HexStr256
    timestamp: datetime = field(
        metadata={
            "deserialize": lambda s: datetime.strptime(s, DATE_FMT),
            "serialize": lambda d: datetime.strftime(d, DATE_FMT),
        },
        default_factory=lambda: datetime.now().astimezone(),
    )
    version: str = "0.7.1"
    checksum_algorithm: str = "SHA256"
    compression_algorithm: str = "gzip"
    transfer_id: Optional[int] = None
    purpose: Optional[Purpose] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MetaData":
        try:
            return deserialize(cls)(d)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid {METADATA_FILE}: {e}") from e

    @classmethod
    def asdict(cls, m: "MetaData") -> Dict[str, Any]:
        dct: Dict[str, Any] = serialize(cls)(m)
        return dct
