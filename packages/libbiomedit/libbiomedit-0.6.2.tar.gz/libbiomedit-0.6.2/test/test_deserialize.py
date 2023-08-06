import unittest
from enum import Enum
from typing import Tuple, Dict, Optional, Any, Sequence, Union
from dataclasses import dataclass

from libbiomedit.lib import deserialize
from libbiomedit.lib.secret import Secret


class TestDeserialize(unittest.TestCase):
    def test_deserialize_dataclass(self) -> None:
        @dataclass
        class Y:
            x: int
            y: Tuple[bool, bool]

        @dataclass
        class X:
            a: int
            pack: Y

        data = {"a": 1, "pack": {"x": 1, "y": [True, False]}}
        x = deserialize.deserialize(X)(data)

        self.assertEqual(x, X(a=1, pack=Y(x=1, y=(True, False))))

        with self.assertRaises(ValueError):
            deserialize.deserialize(Y)({"x": 1, "y": [True]})

    def test_deserialize_dataclass_secret(self) -> None:
        @dataclass
        class Data:
            x: int
            y: Tuple[bool, bool]
            secret: Secret[str]

        data = {"x": 1, "y": [True, False], "secret": "***"}
        x = deserialize.deserialize(Data)(data)

        self.assertEqual(x, Data(x=1, y=(True, False), secret=Secret("***")))

    def test_deserialize_dict(self) -> None:
        @dataclass
        class Z:
            a: int
            dct: Dict[int, str]

        inner = {1: "x", 2: "y"}
        data = {"a": 1, "dct": inner}
        z = deserialize.deserialize(Z)(data)

        self.assertEqual(z, Z(a=1, dct=inner))

    def test_deserialize_optional(self) -> None:
        self.assertEqual(deserialize.deserialize(Optional[int])(None), None)
        self.assertEqual(deserialize.deserialize(Optional[int])(1), 1)
        self.assertEqual(deserialize.deserialize(Any)(1), 1)
        self.assertEqual(deserialize.deserialize(Any)("1"), "1")

    def test_deserialize_tuple(self) -> None:
        with self.assertRaises(ValueError):
            deserialize.deserialize(Tuple[bool, bool])([True])
        self.assertEqual(
            deserialize.deserialize(Tuple[bool, bool])([True, False]), (True, False)
        )
        self.assertEqual(
            deserialize.deserialize(Tuple[bool, ...])([True, False]), (True, False)
        )
        self.assertEqual(deserialize.deserialize(Tuple[bool, ...])([True]), (True,))

    def test_deserialize_enum(self) -> None:
        class Color(Enum):
            RED = "red"
            BLUE = "blue"

        class Number(Enum):
            ONE = 1
            TWO = 2

        self.assertEqual(deserialize.deserialize(Color)("red"), Color.RED)
        self.assertEqual(deserialize.deserialize(Number)(2), Number.TWO)

    def test_deserialize_union(self) -> None:
        @dataclass
        class Y:
            x: int
            y: Tuple[bool, bool]

        @dataclass
        class X:
            a: int

        self.assertEqual(
            deserialize.deserialize(Union[X, Y])(
                {"type": "Y", "value": {"x": 1, "y": [True, True]}}
            ),
            Y(x=1, y=(True, True)),
        )


class TestSerialize(unittest.TestCase):
    def test_serialize_dataclass(self) -> None:
        @dataclass
        class Y:
            x: int
            y: Tuple[bool, bool]

        @dataclass
        class X:
            a: int
            pack: Y

        obj = X(a=1, pack=Y(x=1, y=(True, False)))
        expected = {"a": 1, "pack": {"x": 1, "y": (True, False)}}
        data = deserialize.serialize(X)(obj)

        self.assertEqual(data, expected)

    def test_serialize_dataclass_secret(self) -> None:
        @dataclass
        class Data:
            x: int
            y: Tuple[bool, bool]
            secret: Secret[str]

        with self.assertRaises(ValueError):
            deserialize.serialize(Data)

    def test_serialize_dataclass_optional_secret(self) -> None:
        @dataclass
        class Data:
            x: int
            y: Tuple[bool, bool]
            secret: Optional[Secret[str]]

        obj = Data(x=1, y=(True, False), secret=Secret("***"))
        expected = {"x": 1, "y": (True, False), "secret": None}
        data = deserialize.serialize(Data)(obj)

        self.assertEqual(data, expected)

    def test_serialize_dict(self) -> None:
        @dataclass
        class Z:
            a: int
            dct: Dict[int, str]

        inner = {1: "x", 2: "y"}
        expected = {"a": 1, "dct": inner}
        obj = Z(a=1, dct=inner)
        data = deserialize.serialize(Z)(obj)

        self.assertEqual(data, expected)

    def test_serialize_dict_secret(self) -> None:
        with self.assertRaises(ValueError):
            deserialize.serialize(Dict[str, Secret[Any]])

    def test_serialize_dict_opt_secret(self) -> None:
        data = deserialize.serialize(Dict[str, Optional[Secret[str]]])(
            {"secret": Secret("***")}
        )
        self.assertEqual(data, {"secret": None})

    def test_serialize_dict_secret_any(self) -> None:
        data = deserialize.serialize(Dict[str, Any])({"secret": Secret("***"), "x": 1})
        self.assertEqual(data, {"secret": None, "x": 1})

    def test_serialize_optional(self) -> None:
        self.assertEqual(deserialize.serialize(Optional[int])(None), None)
        self.assertEqual(deserialize.serialize(Optional[int])(1), 1)
        self.assertEqual(deserialize.serialize(Any)(1), 1)
        self.assertEqual(deserialize.serialize(Any)("1"), "1")

    def test_serialize_tuple(self) -> None:
        with self.assertRaises(ValueError):
            deserialize.serialize(Tuple[bool, bool])([True])
        self.assertEqual(
            deserialize.serialize(Tuple[bool, bool])([True, False]), (True, False)
        )
        self.assertEqual(
            deserialize.serialize(Tuple[bool, ...])([True, False]), (True, False)
        )
        self.assertEqual(deserialize.serialize(Tuple[bool, ...])([True]), (True,))

    def test_serialize_tuple_secret(self) -> None:
        with self.assertRaises(ValueError):
            deserialize.serialize(Tuple[Secret])

    def test_serialize_seq_secret(self) -> None:
        with self.assertRaises(ValueError):
            deserialize.serialize(Sequence[Secret[int]])

    def test_deserialize_enum(self) -> None:
        class Color(Enum):
            RED = "red"
            BLUE = "blue"

        class Number(Enum):
            ONE = 1
            TWO = 2

        self.assertEqual(deserialize.serialize(Color)(Color.RED), "red")
        self.assertEqual(deserialize.serialize(Number)(Number.TWO), 2)

    def test_serialize_union(self) -> None:
        @dataclass
        class Y:
            x: int
            y: Tuple[bool, bool]

        @dataclass
        class X:
            a: int

        self.assertEqual(
            deserialize.serialize(Union[X, Y])(Y(x=1, y=(True, True))),
            {"type": "Y", "value": {"x": 1, "y": (True, True)}},
        )
