import pytest
import fractions
import decimal

from copy import deepcopy


@pytest.fixture(scope="session")
def n():
    return 10


@pytest.fixture(scope="session")
def list_len():
    return 10, 20, 100, 1000


@pytest.fixture(scope="session")
def limits():
    return -500, 500


@pytest.fixture(scope="session")
def digits_range():
    return range(10)


@pytest.fixture()
def complex_object():
    obj = {
        "a": 12.22221111,
        "string": "something nice, ha?",
        "callable": lambda x: x ** 2,
        "b": 2,
        "c": 1.222,
        "d": [1.12343, 0.023492],
        "e": {
            "ea": 1 / 44,
            "eb": {1.333, 2.999},
            "ec": dict(eca=1.565656, ecb=1.765765765),
        },
    }
    return deepcopy(obj)

@pytest.fixture()
def object_with_various_numbers():
    obj = {
        "complex number": 1.2-2j,
        "string": "something nice, ha?",
        "callable": lambda x: x ** 2,
        "decimal": decimal.Decimal("1.2"),
        "fraction": fractions.Fraction(1, 4),
    }
    return deepcopy(obj)
