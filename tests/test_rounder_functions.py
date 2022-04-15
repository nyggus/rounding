import pytest
import rounder as r
import random
from copy import deepcopy
from math import ceil, floor

from rounder.rounder import map_object


def test_randomized_tests_round_ceil_floor_object(n, limits, digits_range):
    for _ in range(n):
        x = random.uniform(*limits)
        for digits in digits_range:
            assert round(x, digits) == r.round_object(x, digits)
            assert ceil(x) == r.ceil_object(x)
            assert floor(x) == r.floor_object(x)


def test_use_copy_with_lists_and_dicts():
    items = (
        [222.222, 333.333, 1.000045, "Shout Bamalama!"],
        {"a": 222.222, "b": 333.333, "c": 1.000045, "d": "Shout Bamalama!"},
    )

    for x in items:
        x_rounder_copy = r.round_object(x, 1, True)
        assert x_rounder_copy != x
        x_rounder_no_copy = r.round_object(x, 1, False)
        assert x_rounder_no_copy == x_rounder_copy
        assert x_rounder_no_copy is not x_rounder_copy
        assert x_rounder_no_copy is x


def test_no_copy_with_lists_and_dicts():
    items = (
        [222.222, 333.333, 1.000045, "Shout Bamalama!"],
        {"a": 222.222, "b": 333.333, "c": 1.000045, "d": "Shout Bamalama!"},
    )

    for x in items:
        x_rounder = r.round_object(x, 1)
        assert x_rounder is x


def test_copy_with_tuples_and_sets():
    items = (
        (222.222, 333.333, 1.000045, "Shout Bamalama!"),
        {222.222, 333.333, 1.000045, "Shout Bamalama!"},
    )

    for x in items:
        x_rounder = r.round_object(x, 1, True)
        assert x_rounder is not x
        assert x_rounder != x


def test_no_copy_with_tuples_and_sets():
    items = (
        (222.222, 333.333, 1.000045, "Shout Bamalama!"),
        {222.222, 333.333, 1.000045, "Shout Bamalama!"},
    )

    for x in items:
        x_rounder = r.round_object(x, 1, False)
        assert x_rounder is not x
        assert x_rounder != x


def test_randomized_tests_using_copy_lists_tuples_sets(
    n, list_len, limits, digits_range
):
    for _ in range(n):
        for length in list_len:
            for digits in digits_range:
                for iter_type in (list, tuple, set):
                    x = iter_type(
                        random.uniform(*limits) for i in range(length)
                    )
                    x_copy = deepcopy(x)

                    r_rounded_x = r.round_object(x, digits, use_copy=True)
                    assert r_rounded_x != x

                    rounded_x = iter_type(round(x, digits) for x in x_copy)
                    assert r_rounded_x is not x
                    assert rounded_x == r_rounded_x

                    # use_copy was used, so the original list did not change:
                    # (here, this makes a difference for lists but not for
                    # sets and tuples)
                    if iter_type is list:
                        assert r_rounded_x != x
                        no_copy_r_rounded_x = r.round_object(
                            x, digits, use_copy=False
                        )
                        assert no_copy_r_rounded_x == r_rounded_x

                        # use_copy was NOT used, so the original list DID change:
                        assert r_rounded_x == x


def test_randomized_tests_using_copy_dicts(n, limits, digits_range):
    for _ in range(n):
        for digits in digits_range:
            for iter_type in (list, tuple, set):
                x = {
                    letter: random.uniform(*limits) for letter in "abcefghijk"
                }
                x_copy = deepcopy(x)

                r_rounded_x = r.round_object(x, digits, use_copy=True)
                assert r_rounded_x != x

                rounded_x = {
                    letter: round(x, digits) for letter, x in x_copy.items()
                }
                assert r_rounded_x is not x
                assert rounded_x == r_rounded_x

                # use_copy was used, so the original list did not change:
                assert r_rounded_x != x
                no_copy_r_rounded_x = r.round_object(x, digits, use_copy=False)
                assert no_copy_r_rounded_x == r_rounded_x

                # use_copy was NOT used, so the original list DID change:
                assert r_rounded_x == x


def test_with_non_roundable_items():
    assert r.round_object("Shout Bamalama!") == "Shout Bamalama!"
    assert r.ceil_object("Shout Bamalama!") == "Shout Bamalama!"
    assert r.floor_object("Shout Bamalama!") == "Shout Bamalama!"
    assert r.signif_object("Shout Bamalama!", 5) == "Shout Bamalama!"


def test_with_non_roundable_items_lists():
    assert r.round_object(["Shout Bamalama!"]) == ["Shout Bamalama!"]
    assert r.ceil_object(["Shout Bamalama!"]) == ["Shout Bamalama!"]
    assert r.floor_object(["Shout Bamalama!"]) == ["Shout Bamalama!"]
    assert r.signif_object(["Shout Bamalama!"], 5) == ["Shout Bamalama!"]


def test_with_non_roundable_items_tuples():
    assert r.round_object(("Shout Bamalama!")) == ("Shout Bamalama!")
    assert r.ceil_object(("Shout Bamalama!")) == ("Shout Bamalama!")
    assert r.floor_object(("Shout Bamalama!")) == ("Shout Bamalama!")
    assert r.signif_object(("Shout Bamalama!"), 5) == ("Shout Bamalama!")


def test_with_non_roundable_items_sets():
    assert r.round_object({"Shout Bamalama!"}) == {"Shout Bamalama!"}
    assert r.ceil_object({"Shout Bamalama!"}) == {"Shout Bamalama!"}
    assert r.floor_object({"Shout Bamalama!"}) == {"Shout Bamalama!"}
    assert r.signif_object({"Shout Bamalama!"}, 5) == {"Shout Bamalama!"}


def test_with_non_roundable_items_dicts():
    assert r.round_object({"phrase": "Shout Bamalama!"}) == {
        "phrase": "Shout Bamalama!"
    }
    assert r.ceil_object({"phrase": "Shout Bamalama!"}) == {
        "phrase": "Shout Bamalama!"
    }
    assert r.floor_object({"phrase": "Shout Bamalama!"}) == {
        "phrase": "Shout Bamalama!"
    }
    assert r.signif_object({"phrase": "Shout Bamalama!"}, 5) == {
        "phrase": "Shout Bamalama!"
    }


def test_round_object_for_complex_object(complex_object):
    rounded_complex_object = r.round_object(complex_object, 3, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 12.222
    assert rounded_complex_object["e"] == {
        "ea": 0.023,
        "eb": {1.333, 2.999},
        "ec": {"eca": 1.566, "ecb": 1.766},
    }
    assert rounded_complex_object["d"] == [1.123, 0.023]


def test_ceil_object_for_complex_object(complex_object):
    rounded_complex_object = r.ceil_object(complex_object, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 13
    assert rounded_complex_object["e"] == {
        "ea": 1,
        "eb": {2, 3},
        "ec": {"eca": 2, "ecb": 2},
    }
    assert rounded_complex_object["d"] == [2, 1]


def test_floor_object_for_complex_object(complex_object):
    rounded_complex_object = r.floor_object(complex_object, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 12
    assert rounded_complex_object["e"] == {
        "ea": 0,
        "eb": {1, 2},
        "ec": {"eca": 1, "ecb": 1},
    }
    assert rounded_complex_object["d"] == [1, 0]


def test_signif_object_for_complex_object_3_digits(complex_object):
    rounded_complex_object = r.signif_object(complex_object, 3, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 12.2
    assert rounded_complex_object["e"] == {
        "ea": 0.0227,
        "eb": {1.33, 3.0},
        "ec": {"eca": 1.57, "ecb": 1.77},
    }
    assert rounded_complex_object["d"] == [1.12, 0.0235]


def test_signif_object_for_complex_object_5_digits(complex_object):
    rounded_complex_object = r.signif_object(complex_object, 4, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 12.22
    assert rounded_complex_object["e"] == {
        "ea": 0.02273,
        "eb": {1.333, 2.999},
        "ec": {"eca": 1.566, "ecb": 1.766},
    }
    assert rounded_complex_object["d"] == [1.123, 0.02349]


def test_for_complex_numbers():
    assert r.round_object(1.934643 - 2j, 2) == 1.93 - 2j
    assert r.ceil_object(1.934643 - 2j) == 2 - 2j
    assert r.floor_object(1.934643 - 2j) == 1 - 2j
    assert r.signif_object(1.934643 - 2j, 5) == 1.9346 - 2j


def test_signif_floats():
    assert r.signif(1.444555, 1) == 1.0
    assert r.signif(1.444555, 2) == 1.4
    assert r.signif(1.444555, 3) == 1.44
    assert r.signif(1.444555, 4) == 1.445
    assert r.signif(1.444555, 5) == 1.4446
    assert r.signif(1.444555, 6) == 1.44456
    assert r.signif(1.444555, 7) == 1.444555
    assert r.signif(1.444555, 8) == 1.444555


def test_signif_ints():
    assert r.signif(1444555, 1) == 1000000
    assert r.signif(1444555, 2) == 1400000
    assert r.signif(1444555, 3) == 1440000
    assert r.signif(1444555, 4) == 1445000
    assert r.signif(1444555, 5) == 1444600
    assert r.signif(1444555, 6) == 1444560
    assert r.signif(1444555, 7) == 1444555
    assert r.signif(1444555, 8) == 1444555


def test_signif_exception():
    with pytest.raises(r.NonNumericTypeError):
        r.signif("string", 3)

    with pytest.raises(r.NonNumericTypeError):
        r.signif([2.12], 3)

    with pytest.raises(r.NonNumericTypeError):
        r.signif((1,), 3)


def test_with_unpickable_objects():
    gen = (i ** 2 for i in range(10))
    with pytest.raises(r.UnpickableObjectError):
        _ = r.round_object(gen, use_copy=True)
    _ = r.round_object(gen, use_copy=False)


def test_with_callable():
    f = lambda x: x
    assert callable(r.round_object(f))

    def f():
        pass

    x = {"items": [1.1222, 1.343434], "function": f}
    assert callable(x["function"])

    x_rounded = r.round_object(x, 2, use_copy=True)
    assert callable(x_rounded["function"])

    x_ceil = r.ceil_object(x, use_copy=True)
    assert callable(x_ceil["function"])

    x_floor = r.floor_object(x, use_copy=True)
    assert callable(x_floor["function"])

    x_signif = r.signif_object(x, 3, use_copy=True)
    assert callable(x_signif["function"])


def test_map_object_basic():
    x = [1.12, 1.13]
    assert r.map_object(lambda x: x, x, False) is x
    assert r.map_object(lambda x: x, x, True) is not x
    assert r.map_object(lambda x: x, x, True) == x


def test_map_object_exception():
    with pytest.raises(r.NonCallableError):
        r.map_object(2, 2)
    with pytest.raises(r.NonCallableError):
        r.map_object((lambda x: x)(2), 2)
    with pytest.raises(r.NonCallableError):
        r.map_object([], [2, 2])


def test_map_object_dicts_lists():
    obj = {
        "list": [1.44, 2.67, 3.334, 6.665],
        "main value": 5.55,
        "explanation": "to be filled in",
    }
    negative_reversed_obj = r.signif_object(
        r.map_object(lambda x: -1 / x, obj, True), 5
    )
    assert negative_reversed_obj == {
        "list": [-0.69444, -0.37453, -0.29994, -0.15004],
        "main value": -0.18018,
        "explanation": "to be filled in",
    }


def test_map_object_squared(complex_object):
    squared_complex_object = r.round_object(
        r.map_object(lambda x: x * x, complex_object, True), 3
    )
    assert squared_complex_object["a"] == 149.382
    assert squared_complex_object["e"] == {
        "ea": 0.001,
        "eb": {8.994, 1.777},
        "ec": {"eca": 2.451, "ecb": 3.118},
    }
    assert squared_complex_object["d"] == [1.262, 0.001]


def test_with_class_instance():
    class A:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    a = A(
        x=10.0001,
        y=(44.4444, 55.5555, 66.6666, {"item1": 456.654, "item2": 90.0004}),
    )
    assert r.round_object(a.x, 0, True) == 10
    assert r.round_object(a.y[:3], 0, True) == (44, 56, 67)
    assert r.round_object(a.y[3], 0, True) == {"item1": 457, "item2": 90}

    a_copy = r.signif_object(a, 4, True)
    assert a_copy.x == 10
    assert a_copy.y[:3] == (44.44, 55.56, 66.67)
    assert a_copy.y[3] == {"item1": 456.7, "item2": 90}

    # Note that you cannot create a copy of a class instance's attribute
    # and change it inplace in the instance:
    _ = r.map_object(lambda x: x * 2, a_copy.x)
    assert a_copy.x != 20 and a_copy.x == 10

    _ = r.ceil_object(a)
    assert a.x == 11
    assert a.y[:3] == (45, 56, 67)
    assert a.y[3] == {"item1": 457, "item2": 91}


def test_for_namedtuples():
    from collections import namedtuple

    X = namedtuple("X", "a b c")

    x1 = X(12.12, 13.13, 14.94)
    x1_rounded_copy = r.round_object(x1, 0, True)
    assert x1_rounded_copy == X(12, 13, 15)
    x1_rounded_no_copy = r.round_object(x1, 0, False)
    assert x1_rounded_no_copy == X(12, 13, 15)
    assert x1 == X(12.12, 13.13, 14.94)

    x2 = X(
        a=12.13,
        b=[44.4444, 55.5555, 66.6666],
        c={"item1": 457.1212, "item2": 90.0001},
    )

    assert r.round_object(x2.a, 0) == 12
    assert r.round_object(x2.b, 0) == [44, 56, 67]
    assert r.round_object(x2.c, 0) == {"item1": 457, "item2": 90}

    assert r.signif_object(x2, 4) == X(
        a=12.13, b=[44.0, 56.0, 67.0], c={"item1": 457.0, "item2": 90.0}
    )

    assert r.map_object(lambda x: r.signif(x * 2, 2), x2) == X(
        a=24.0, b=[88.0, 110.0, 130.0], c={"item1": 910.0, "item2": 180.0}
    )


def test_for_NamedTuples():
    from typing import NamedTuple

    X1 = NamedTuple("X1", [("a", float), ("b", tuple), ("c", dict)])

    x1 = X1(12.12, 13.13, 14.94)
    x1_rounded_copy = r.round_object(x1, 0, True)
    assert x1_rounded_copy == X1(12, 13, 15)
    x1_rounded_no_copy = r.round_object(x1, 0, False)
    assert x1_rounded_no_copy == X1(12, 13, 15)
    assert x1 == X1(12.12, 13.13, 14.94)

    X2 = NamedTuple("X2", [("a", float), ("b", tuple), ("c", dict)])
    x2 = X2(
        a=12.13,
        b=[44.4444, 55.5555, 66.6666],
        c={"item1": 457.1212, "item2": 90.0001},
    )

    assert r.round_object(x2.a, 0) == 12
    assert r.round_object(x2.b, 0) == [44, 56, 67]
    assert r.round_object(x2.c, 0) == {"item1": 457, "item2": 90}

    assert r.signif_object(x2, 4) == X2(
        a=12.13, b=[44.0, 56.0, 67.0], c={"item1": 457.0, "item2": 90.0}
    )

    assert r.map_object(lambda x: r.signif(x * 2, 2), x2) == X2(
        a=24.0, b=[88.0, 110.0, 130.0], c={"item1": 910.0, "item2": 180.0}
    )


def test_for_OrderedDict():
    from collections import OrderedDict

    d = OrderedDict(a=1.1212, b=55.559)

    d_rounded_copy = r.round_object(d, 2, True)
    assert d_rounded_copy == OrderedDict(a=1.12, b=55.56)
    assert d == OrderedDict(a=1.1212, b=55.559)

    d_rounded_no_copy = r.round_object(d, 2, False)
    assert d_rounded_no_copy == OrderedDict(a=1.12, b=55.56)
    assert d == OrderedDict(a=1.12, b=55.56)

    d = OrderedDict(
        a=1.1212,
        b=55.559,
        c={"item1": "string", "item2": 3434.3434},
        d=OrderedDict(d1=3434.3434, d2=[99.99, 1.2323 - 2j]),
    )

    d_rounded_copy = r.round_object(d, 2, True)
    assert d_rounded_copy == OrderedDict(
        [
            ("a", 1.12),
            ("b", 55.56),
            ("c", {"item1": "string", "item2": 3434.34}),
            (
                "d",
                OrderedDict([("d1", 3434.34), ("d2", [99.99, (1.23 - 2j)])]),
            ),
        ]
    )
    assert d != d_rounded_copy

    d_rounded_no_copy = r.round_object(d, 2, False)
    assert d_rounded_no_copy == d_rounded_copy
    assert d_rounded_no_copy == d
