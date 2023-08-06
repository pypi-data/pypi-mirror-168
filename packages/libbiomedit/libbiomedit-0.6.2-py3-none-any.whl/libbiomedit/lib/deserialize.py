from typing import (
    Union,
    Tuple,
    List,
    Any,
    Dict,
    Optional,
    Sequence,
    cast,
    Callable,
    Type,
    TypeVar,
    get_type_hints,
    overload,
)
import collections.abc
import warnings
from enum import Enum

import dataclasses

from .classify import (
    classify,
    __origin_attr__,
    AbstractType as AbstractType,
    IsDataclass,
    IsTypingType,
    is_secret,
)
from .secret import Secret

Tp = TypeVar("Tp")
Transform = Callable[[Any], Any]
TransformFactory = Callable[[Tp], Transform]


@overload
def deserialize(T: Type[Tp]) -> Callable[[Any], Tp]:
    ...


@overload
def deserialize(T: Tp) -> Callable[[Any], Tp]:
    """This overload is needed due to https://github.com/python/mypy/issues/9003"""


def deserialize(T: Union[Type[Tp], Tp]) -> Callable[[Any], Tp]:
    """Creates a deserializer for the type :T:. It handles dataclasses,
    sequences, typing.Optional, Enum and primitive types.

    :returns: A deserializer, converting a dict, list or primitive to :T:
    """

    def des(x: Transform) -> Transform:
        return x

    return _deserializers.get(classify(T), des)(T)


@overload
def serialize(T: Type[Tp]) -> Callable[[Tp], Any]:
    ...


@overload
def serialize(T: Tp) -> Callable[[Tp], Any]:
    """This overload is needed due to https://github.com/python/mypy/issues/9003"""


def serialize(T: Union[Type[Tp], Tp]) -> Callable[[Tp], Any]:
    """Creates a serializer for the type :T:. It handles dataclasses,
    sequences, typing.Optional, Enum and primitive types.

    :returns: A serializer, converting an instance of :T: to dict, list or primitive
    """

    def ser(x: Transform) -> Transform:
        return x

    return _serializers.get(classify(T), ser)(T)


_deserializers = {}
_serializers = {}


def _deserializer(
    T: Union[type, object]
) -> Callable[[TransformFactory[Any]], TransformFactory[Any]]:
    def decorator(f: TransformFactory[Any]) -> TransformFactory[Any]:
        _deserializers[T] = f
        return f

    return decorator


def _serializer(
    T: Union[type, object]
) -> Callable[[TransformFactory[Any]], TransformFactory[Any]]:
    def decorator(f: TransformFactory[Any]) -> TransformFactory[Any]:
        _serializers[T] = f
        return f

    return decorator


def _serializer_deserializer(
    T: Any,
) -> Callable[[Transform], Transform]:
    def decorator(f: Transform) -> Transform:
        _deserializers[T] = f(deserialize)
        _serializers[T] = f(serialize)
        return f

    return decorator


@_deserializer(Any)
def deserialize_any(_: AbstractType) -> Transform:
    return lambda x: x


@_serializer(Any)
def serialize_any(_: AbstractType) -> Transform:
    def _serialize(x: Any) -> Any:
        if isinstance(x, Secret):
            raise RuntimeError(
                "Trying to implicitly serialize a Secret. Try using Optional[Secret]."
            )

        return x

    return _serialize


@_deserializer(Secret)
def deserialize_secret(T: Type[Secret[Any]]) -> Callable[[Any], Secret[Any]]:
    inner_deserialize = deserialize(getattr(T, "__args__", (Any,))[0])
    return lambda val: Secret(inner_deserialize(val))


@_serializer(Secret)
def serialize_secret(_: AbstractType) -> Callable[[Type[Secret[Any]]], None]:
    def _serialize(_: Type[Secret[Any]]) -> None:
        raise RuntimeError(
            "Trying to explicitly serialize a Secret. This should not happen."
        )

    return _serialize


@_serializer_deserializer(Tuple)
def transform_tuple(
    transform: TransformFactory[AbstractType],
) -> Callable[[IsTypingType], Transform]:
    def _transform_tuple(T: IsTypingType) -> Transform:
        item_types: Tuple[AbstractType, ...] = T.__args__
        if transform is serialize and any(
            is_secret(item_type) for item_type in item_types
        ):
            raise ValueError(
                "Serializing tuples containing Secret is not supported. Try using Optional[Secret]"
            )

        if len(item_types) == 2 and cast(Any, item_types[1]) is ...:
            inner_transform = transform(item_types[0])

            def _transform_ellipsis(data: Tuple[Any, ...]) -> Tuple[Any, ...]:
                return tuple(inner_transform(item) for item in data)

            return _transform_ellipsis

        inner_transforms = [transform(T) for T in item_types]

        def _transform(data: Tuple[Any, ...]) -> Tuple[Any, ...]:
            if len(item_types) != len(data):
                raise ValueError(f"Wrong number ({len(data)}) of items for {repr(T)}")
            return tuple(
                inner_transform(item)
                for inner_transform, item in zip(inner_transforms, data)
            )

        return _transform

    return _transform_tuple


@_serializer_deserializer(Sequence)
def transform_seq(
    transform: TransformFactory[AbstractType],
) -> Callable[[IsTypingType], Transform]:
    def _transform_seq(T: IsTypingType) -> Transform:
        try:
            seq_type: Union[Type[List[Any]], Type[Tuple[Any, ...]]] = getattr(
                T, __origin_attr__
            )
        except AttributeError as e:
            raise ValueError(f"Unexpected type {T}") from e
        try:
            item_type = T.__args__[0]
        except AttributeError as e:
            raise ValueError(
                f"Sequence of type {seq_type.__name__} without item type"
            ) from e
        if transform is serialize and is_secret(item_type):
            raise ValueError(
                "Serializing sequences of Secret is not supported. try using Optional[Secret]"
            )
        if seq_type is collections.abc.Sequence:
            seq_type = list

        def _transform(data: Sequence[Any]) -> Sequence[Any]:
            return seq_type(map(transform(item_type), data))

        return _transform

    return _transform_seq


@_deserializer(IsDataclass)
def deserialize_dataclass(T: IsDataclass) -> Transform:
    deserializers_by_name = prepare_serializers(T, deserialize)

    def _deserialize(data: Dict[str, Any]) -> Any:
        unexpected_keys = set(data) - set(n for n, _ in deserializers_by_name)
        if unexpected_keys:
            warnings.warn(
                f"{T.__name__}: Unexpected keys: " + ", ".join(unexpected_keys)
            )
        converted_data = {
            f_name: deserializer(data[f_name])
            for f_name, deserializer in deserializers_by_name
            if f_name in data
        }
        return T(**converted_data)

    return _deserialize


@_serializer(IsDataclass)
def serialize_dataclass(T: IsDataclass) -> Transform:
    serializers_by_name = prepare_serializers(T, serialize)
    if any(is_secret(f.type) for f in dataclasses.fields(T)):
        raise ValueError(
            "Serializing dataclasses with Secret values are not supported. Try using Optional[Secret]."
        )

    def _serialize(obj: Any) -> Dict[str, Any]:
        converted_data = {
            f_name: serializer(getattr(obj, f_name))
            for f_name, serializer in serializers_by_name
        }
        return converted_data

    return _serialize


def prepare_serializers(
    T: IsDataclass, transform: TransformFactory[Any]
) -> Sequence[Tuple[str, Transform]]:
    fields = dataclasses.fields(T)
    type_hints = get_type_hints(T)
    return [
        (f.name, transform(f.metadata.get(transform.__name__, type_hints[f.name])))
        for f in fields
    ]


@_serializer_deserializer(Optional)
def transform_optional(
    transform: TransformFactory[AbstractType],
) -> TransformFactory[IsTypingType]:
    def _transform_optional(T: IsTypingType) -> Transform:
        opt_type = optional_type(T)

        if is_secret(opt_type) and transform is serialize:
            return lambda _: None

        inner_transform = transform(opt_type)

        def _transform(data: Optional[Any]) -> Optional[Any]:
            return None if data is None else inner_transform(data)

        return _transform

    return _transform_optional


def optional_type(T: IsTypingType) -> type:
    return next(
        t for t in T.__args__ if not (isinstance(t, type) and isinstance(None, t))
    )


@_deserializer(Union)
def deserialize_union(T: IsTypingType) -> Transform:
    """Deserializes Unions of dataclasses.
    The variants are assumed to be adjacently tagged by its type ("type" and "value")."""
    types = T.__args__
    if not all(dataclasses.is_dataclass(t) for t in types):
        raise ValueError("Currently, only Unions of dataclasses are supported")
    transform_by_name: Dict[str, Transform] = {
        t.__name__: deserialize(t) for t in types
    }

    def _deserialize(data: Dict[str, Any]) -> Any:
        type_name = data.get("type")
        if type_name is None:
            raise ValueError(
                f"Union[{', '.join(transform_by_name)}]: missing `type` item"
            )
        inner_transform = transform_by_name.get(type_name)
        if inner_transform is None:
            raise ValueError(
                f"Union[{', '.join(transform_by_name)}]: "
                f"unexpected type `{type_name}`"
            )
        return inner_transform(data["value"])

    return _deserialize


@_serializer(Union)
def serialize_union(T: IsTypingType) -> Transform:
    """Serializes Unions of dataclasses.
    The variants are adjacently tagged by its type ("type" and "value")."""
    types = T.__args__
    if not all(dataclasses.is_dataclass(t) for t in types):
        raise ValueError("Currently, only Unions of dataclasses are supported")
    transform_by_type: Dict[type, Transform] = {t: serialize(t) for t in types}

    def _serialize(data: Any) -> Dict[str, Any]:
        inner_type = type(data)
        inner_serialize = transform_by_type.get(inner_type)
        if inner_serialize is None:
            variants = ", ".join(t.__name__ for t in transform_by_type)
            raise ValueError(
                f"{data}: Could associate {inner_type.__name__} to one of the variants {variants}"
            )
        return {"type": inner_type.__name__, "value": inner_serialize(data)}

    return _serialize


def transform_dict(
    transform: TransformFactory[Any],
) -> TransformFactory[IsTypingType]:
    def _transform_dict(T: IsTypingType) -> Callable[[Dict[Any, Any]], Dict[Any, Any]]:
        key_type, val_type = T.__args__

        if transform is serialize and is_secret(val_type):
            raise ValueError(
                "Serializing dicts with Secret values is not supported. Use Optional[Secret]."
            )

        key_transform = transform(key_type)
        val_transform = transform(val_type)

        def _transform(data: Dict[Any, Any]) -> Dict[Any, Any]:
            return {key_transform(key): val_transform(val) for key, val in data.items()}

        return _transform

    return _transform_dict


@_serializer(Dict)
def serialize_dict(T: IsTypingType) -> Transform:
    """Special serializer to support dict[str, Any] holding Secret values.
    In this case Secret is interpreted as Optional[Secret] and serialized to None."""
    raw_serialize: Callable[[Dict[Any, Any]], Dict[Any, Any]] = transform_dict(
        serialize
    )(T)

    def _serialize(obj: Dict[Any, Any]) -> Dict[Any, Any]:
        return raw_serialize(
            {
                key: val if not isinstance(val, Secret) else None
                for key, val in obj.items()
            }
        )

    return _serialize


@_deserializer(Dict)
def deserialize_dict(T: IsTypingType) -> Transform:
    return transform_dict(deserialize)(T)


@_serializer(Enum)
def serialize_enum(_T: Type[Enum]) -> Transform:
    def _serialize(obj: Enum) -> Any:
        return obj.value

    return _serialize
