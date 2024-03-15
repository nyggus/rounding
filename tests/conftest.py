import decimal
import fractions
import random
from copy import deepcopy

import pytest


N_OF_TESTS = 3
LIMITS = [(-500, 500), (-0.1, 0.1)]
N_OF_DIGITS = range(7)
OBJECT_LENGTHS = [10, 100, 1000, 100_000]


@pytest.fixture(params=[tuple, set, list])
def iter_type(request):
    return request.param


@pytest.fixture(params=OBJECT_LENGTHS)
def length(request):
    return request.param


@pytest.fixture(params=[None] * N_OF_TESTS)
def randomize(request):
    return request.param


@pytest.fixture(params=LIMITS)
def limits(request):
    return request.param


@pytest.fixture
def x(randomize, limits):
    return random.uniform(*limits)


@pytest.fixture(scope="session", params=N_OF_DIGITS)
def n_of_digits(request):
    return request.param


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
        "complex number": 1.2 - 2j,
        "string": "something nice, ha?",
        "callable": lambda x: x ** 2,
        "decimal": decimal.Decimal("1.2"),
        "fraction": fractions.Fraction(1, 4),
    }
    return deepcopy(obj)


@pytest.fixture(
    params=[
        [222.222, 333.333, 1.000045, "Shout Bamalama!"],
        [222.222, [333.333, 444.444, 5555.5555], 1.000045, "Shout Bamalama!"],
    ]
)
def obj_list(request):
    return request.param


@pytest.fixture(
    params=[
        {"a": 222.222, "b": 333.333, "c": 1.000045, "d": "Shout Bamalama!"},
        {
            "a": 222.222,
            "b": [333.333, 444.444, 5555.5555],
            "c": 1.000045,
            "d": "Shout Bamalama!",
        },
    ]
)
def obj_dict(request):
    return request.param


@pytest.fixture(
    params=[
        {222.222, 333.333, 1.000045, "Shout Bamalama!"},
        {222.222, (333.333, 444.444, 5555.5555), 1.000045, "Shout Bamalama!"},
    ]
)
def obj_set(request):
    return request.param


@pytest.fixture(
    params=[
        (222.222, 333.333, 1.000045, "Shout Bamalama!"),
        (222.222, (333.333, 444.444, 5555.5555), 1.000045, "Shout Bamalama!"),
    ]
)
def obj_tuple(request):
    return request.param
