import sys
from typing import Union, Tuple, Any, Dict, Optional, Sequence, Callable, Type
from enum import Enum
import collections.abc
from abc import ABC

import dataclasses

from .secret import Secret


# Starting with python 3.7, the typing module has a new API
__origin_attr__ = "__extra__" if sys.version_info < (3, 7) else "__origin__"

_classifiers = []


class IsDataclass(type):
    __dataclass_fields__: Dict[
        str, "dataclasses.Field[Any]"
    ]  # TODO: unquote typehint, once we require python >= 3.9


class IsTypingType(ABC):
    __args__: Tuple[type, ...]


AbstractType = Union[IsDataclass, IsTypingType, type, Type[Enum], object]


def _classifier(
    T: Union[type, object],
) -> Callable[[Callable[[AbstractType], bool]], Callable[[AbstractType], bool]]:
    """Decorator populating :_classifiers:"""

    def decorator(f: Callable[[AbstractType], bool]) -> Callable[[AbstractType], bool]:
        _classifiers.append((T, f))
        return f

    return decorator


def classify(T: AbstractType) -> Union[type, object]:
    try:
        return next(C for C, check in _classifiers if check(T))
    except StopIteration:
        return None


@_classifier(Any)
def is_any(T: AbstractType) -> bool:
    return T is Any


@_classifier(Secret)
def is_secret(T: AbstractType) -> bool:
    return _is_raw_secret(getattr(T, "__origin__", object)) or _is_raw_secret(T)


def _is_raw_secret(T: AbstractType) -> bool:
    return isinstance(T, type) and issubclass(T, Secret)


@_classifier(Tuple)
def is_tuple(T: AbstractType) -> bool:
    return getattr(T, __origin_attr__, None) is tuple


@_classifier(Sequence)
def is_seq(T: AbstractType) -> bool:
    seq_type = getattr(T, __origin_attr__, None)
    return isinstance(seq_type, type) and issubclass(seq_type, collections.abc.Sequence)


@_classifier(IsDataclass)
def is_dataclass(T: AbstractType) -> bool:
    return dataclasses.is_dataclass(T)


@_classifier(Optional)
def is_optional(T: AbstractType) -> bool:
    return (
        getattr(T, "__origin__", None) is Union
        and type(None) in getattr(T, "__args__", ())
        and len(getattr(T, "__args__", ())) == 2
    )


@_classifier(Enum)
def is_enum(T: AbstractType) -> bool:
    return isinstance(T, type) and issubclass(T, Enum)


@_classifier(Union)
def is_union(T: AbstractType) -> bool:
    return getattr(T, "__origin__", None) is Union


@_classifier(Dict)
def is_dict(T: AbstractType) -> bool:
    t_origin = getattr(T, __origin_attr__, None)
    return t_origin is dict
