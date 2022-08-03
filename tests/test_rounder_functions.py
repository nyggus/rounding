import asyncio
import pytest
import rounder as r
import random
from copy import deepcopy
from math import ceil, floor


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
        x_rounded_copy = r.round_object(x, 1, True)
        assert x_rounded_copy != x
        x_rounded_no_copy = r.round_object(x, 1, False)
        assert x_rounded_no_copy == x_rounded_copy
        assert x_rounded_no_copy is not x_rounded_copy
        assert x_rounded_no_copy is x


def test_no_copy_with_lists_and_dicts():
    items = (
        [222.222, 333.333, 1.000045, "Shout Bamalama!"],
        {"a": 222.222, "b": 333.333, "c": 1.000045, "d": "Shout Bamalama!"},
    )

    for x in items:
        x_rounded = r.round_object(x, 1)
        assert x_rounded is x


def test_copy_with_tuples_and_sets():
    items = (
        (222.222, 333.333, 1.000045, "Shout Bamalama!"),
        {222.222, 333.333, 1.000045, "Shout Bamalama!"},
    )

    for x in items:
        x_rounded = r.round_object(x, 1, True)
        assert x_rounded is not x
        assert x_rounded != x


def test_no_copy_with_tuples_and_sets():
    items = (
        (222.222, 333.333, 1.000045, "Shout Bamalama!"),
        {222.222, 333.333, 1.000045, "Shout Bamalama!"},
    )

    for x in items:
        x_rounded = r.round_object(x, 1, False)
        assert x_rounded is not x
        assert x_rounded != x


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


def test_with_callable():
    def f(x):
        return x

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
    r.map_object(lambda x: x * 2, a_copy.x)
    assert a_copy.x == 10

    r.ceil_object(a)
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


def test_for_defaultdict():
    from collections import defaultdict

    d = defaultdict(list)
    d["a"] = 1.1212
    d["b"] = 55.55656
    d["c"] = 0.104343

    d_rounded_copy = r.round_object(d, 2, True)

    assert d_rounded_copy == defaultdict(a=1.12, b=55.56, c=0.10)
    assert d != d_rounded_copy

    d_rounded_no_copy = r.round_object(d, 2, False)
    assert d_rounded_no_copy == defaultdict(a=1.12, b=55.56, c=0.10)
    assert d == d_rounded_no_copy


def test_for_UserDict():
    from collections import UserDict

    d = UserDict(dict(a=1.1212, b=55.559))

    d_rounded_copy = r.round_object(d, 2, True)
    assert d_rounded_copy == UserDict(dict(a=1.12, b=55.56))
    assert d == UserDict(dict(a=1.1212, b=55.559))
    assert type(d_rounded_copy) == UserDict

    d_rounded_no_copy = r.round_object(d, 2, False)
    assert d_rounded_no_copy == UserDict(dict(a=1.12, b=55.56))
    assert d == UserDict(dict(a=1.12, b=55.56))

    d = UserDict(
        dict(
            a=1.1212,
            b=55.559,
            c={"item1": "string", "item2": 3434.3434},
            d=UserDict(dict(d1=3434.3434, d2=[99.996, 1.2323 - 2j])),
        )
    )

    d_rounded_copy = r.round_object(d, 2, True)
    d_rounded_copy = UserDict(
        dict(
            a=1.12,
            b=55.56,
            c={"item1": "string", "item2": 3434.34},
            d=UserDict(dict(d1=3434.34, d2=[100.0, 1.23 - 2j])),
        )
    )

    assert d != d_rounded_copy
    assert type(d_rounded_copy) == UserDict

    d_rounded_no_copy = r.round_object(d, 2, False)
    assert d_rounded_no_copy == d_rounded_copy
    assert d_rounded_no_copy == d


def test_for_deque():
    from collections import deque

    d = deque([1.1222, 3.9989, 4.005])

    d_rounded_copy = r.round_object(d, 2, True)

    assert d_rounded_copy == deque([1.12, 4.0, 4.0])
    assert d != d_rounded_copy

    d_rounded_no_copy = r.round_object(d, 2, False)
    assert d_rounded_no_copy == deque([1.12, 4.0, 4.0])
    assert d == d_rounded_no_copy


def test_for_Counter():
    from collections import Counter

    d = Counter([1.1222, 1.2222, 4.005])

    d_rounded_copy = r.map_object(lambda x: 2 * x, d, True)
    assert d_rounded_copy == Counter({1.1222: 2, 1.2222: 2, 4.005: 2})

    d_rounded_no_copy = r.map_object(lambda x: 2 * x, d, False)
    assert d_rounded_no_copy is d

    d = Counter([1, 1, 2] + [5] * 12222)
    d_rounded_copy = r.round_object(d, 2, True)
    assert d_rounded_copy == d
    d_rounded_copy = r.signif_object(d, 2, True)
    assert d_rounded_copy != d
    assert d_rounded_copy == Counter({1: 2, 2: 1, 5: 12000})


def test_copy_for_frozenset():
    x = frozenset(
        [
            222.222,
            333.333,
            1.000045,
            "Shout Bamalama!",
            222.222,
            333.333,
            1.000045,
            "Shout Bamalama",
        ]
    )

    x_rounded = r.round_object(x, 1, True)
    assert x_rounded is not x
    assert x_rounded != x


def test_no_copy_for_frozenset():
    x = frozenset(
        [
            222.222,
            333.333,
            1.000045,
            "Shout Bamalama!",
            222.222,
            333.333,
            1.000045,
            "Shout Bamalama",
        ]
    )

    x_rounded = r.round_object(x, 1, False)
    assert x_rounded is not x
    assert x_rounded == frozenset(
        {1.0, "Shout Bamalama!", 333.3, "Shout Bamalama", 222.2}
    )


def test_copy_for_bool():
    x = True
    x_rounded = r.round_object(x, use_copy=True)
    assert x_rounded is not x
    assert x_rounded

    y = False
    y_rounded = r.round_object(y, use_copy=True)
    assert y_rounded is not y
    assert not y_rounded


def test_no_copy_for_bool():
    x = True
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is not x
    assert x_rounded

    y = False
    y_rounded = r.round_object(y, use_copy=False)
    assert y_rounded is not y
    assert not y_rounded


def test_copy_for_Decimal():
    from decimal import Decimal

    x = Decimal(1) / Decimal(7)
    x_rounded = r.round_object(x, 4, use_copy=True)
    assert x is not x_rounded
    assert x_rounded == Decimal("0.1429")


def test_no_copy_for_Decimal():
    from decimal import Decimal

    x = Decimal(1) / Decimal(7)
    x_rounded = r.round_object(x, 4, use_copy=False)
    assert x is not x_rounded
    assert x_rounded == Decimal("0.1429")


def test_copy_for_Fraction():
    from fractions import Fraction

    x = Fraction(1, 7)
    x_rounded = r.round_object(x, 4, use_copy=True)
    assert x is not x_rounded
    assert x_rounded == Fraction(1429, 10000)


def test_no_copy_for_Fraction():
    from fractions import Fraction

    x = Fraction(1, 7)
    x_rounded = r.round_object(x, 4, use_copy=False)
    assert x is not x_rounded
    assert x_rounded == Fraction(1429, 10000)


def test_copy_for_None():
    x = None
    x_rounded = r.round_object(x, 4, use_copy=True)
    assert x is x_rounded  # as both are None


def test_no_copy_for_None():
    x = None
    x_rounded = r.round_object(x, 4, use_copy=False)
    assert x is x_rounded


def test_copy_for_coroutine():
    async def ff():
        await asyncio.sleep(0.05)

    x_rounded = r.round_object(ff, use_copy=True)
    assert x_rounded is ff


def test_no_copy_for_coroutine():
    async def ff():
        await asyncio.sleep(0.05)

    x_rounded = r.round_object(ff, use_copy=False)
    assert x_rounded is ff  # copies are not created in the case of coroutines


def test_copy_for_BuiltinFunctionType():
    x = sum
    x_rounded = r.round_object(x, use_copy=True)
    assert x_rounded is sum


def test_no_copy_for_BuiltinFunctionType():
    x = sum
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is sum


def test_copy_for_NotImplementedType():
    x = NotImplemented
    x_rounded = r.round_object(x, use_copy=True)
    assert x_rounded is NotImplemented


def test_no_copy_for_NotImplementedType():
    x = NotImplemented
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is NotImplemented


def test_copy_for_MethodDescriptorType():
    x = str.join
    x_rounded = r.round_object(x, use_copy=True)
    assert x_rounded is x


def test_no_copy_for_MethodDescriptorType():
    x = str.join
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is x


def test_copy_for_EllipsisType():
    x = ...
    x_rounded = r.round_object(x, use_copy=True)
    assert x_rounded is x


def test_no_copy_for_EllipsisType():
    x = ...
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is x


def test_no_copy_for_FrameType():
    import inspect

    x = inspect.currentframe()
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is x


def test_copy_for_MemberDescriptorType():
    class Whatever:
        __slots__ = ("whatever",)

    x = Whatever.__dict__["whatever"]
    x_rounded = r.round_object(x, use_copy=True)
    assert x_rounded is x


def test_no_copy_for_MemberDescriptorType():
    class Whatever:
        __slots__ = ("whatever",)

    x = Whatever.__dict__["whatever"]
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is x


def test_copy_for_BuiltinMethodType():
    from datetime import date

    x = date.today
    x_rounded = r.round_object(x, use_copy=True)
    assert x_rounded is x


def test_no_copy_for_BuiltinMethodType():
    from datetime import date

    x = date.today
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is x


def test_copy_for_MethodWrapperType():
    class Whatever:
        pass

    x = Whatever.__eq__
    x_rounded = r.round_object(x, use_copy=True)
    assert x_rounded is x


def test_no_copy_for_MethodWrapperType():
    class Whatever:
        pass

    x = Whatever.__eq__
    x_rounded = r.round_object(x, use_copy=False)
    assert x_rounded is x


def test_signif_edge_case():
    assert r.signif(123123123123.0002, 7) == 123123100000
    assert r.signif_object(123123123123.0002, 7) == 123123100000


def test_range():
    rng = range(8, 12)
    assert list(r.signif_object(rng, 1)) == [8.0, 9.0, 10, 10]
    assert list(r.signif_object(rng, 1)) == [8.0, 9.0, 10, 10]

    assert list(r.signif_object(rng, 1, True)) == [8.0, 9.0, 10, 10]
    assert list(r.signif_object(rng, 1, True)) == [8.0, 9.0, 10, 10]


def test_filter():
    flt = filter(lambda x: x >= 8, range(12))
    assert list(r.signif_object(flt, 1)) == [8.0, 9.0, 10, 10]
    assert list(r.signif_object(flt, 1)) == []

    flt = filter(lambda x: x >= 8, range(12))
    assert list(r.signif_object(flt, 1, True)) == [8.0, 9.0, 10, 10]
    assert list(r.signif_object(flt, 1)) == [8.0, 9.0, 10, 10]


def test_generator():
    gen = (x for x in range(8, 12))
    assert list(r.signif_object(gen, 1)) == [8.0, 9.0, 10, 10]
    assert list(r.signif_object(gen, 1)) == []

    gen = (x for x in range(8, 12))
    assert list(r.signif_object(gen, 1, True)) == [
        8.0,
        9.0,
        10,
        10,
    ]  # for generators use_copy is ignored
    assert list(r.signif_object(gen, 1)) == []


def test_copy_for_map():
    m = map(lambda i: i / 3, range(10))
    m_rounded_copy = r.round_object(m, 1, use_copy=True)
    assert list(m_rounded_copy) == [
        0.0,
        0.3,
        0.7,
        1.0,
        1.3,
        1.7,
        2.0,
        2.3,
        2.7,
        3.0,
    ]
    assert len(list(m)) == 10


def test_no_copy_for_map_without_copy():
    m = map(lambda i: i / 3, range(10))
    m_rounded_no_copy = r.round_object(m, 1, use_copy=False)
    assert list(m_rounded_no_copy) == [
        0.0,
        0.3,
        0.7,
        1.0,
        1.3,
        1.7,
        2.0,
        2.3,
        2.7,
        3.0,
    ]
    assert len(list(m)) == 0


def test_copy_complex_object_with_map():
    obj = {
        "list": [1.122, 55.55554, 234.3],
        "float": 1.11122156,
        "int": 1212,
        "dict": {
            "filter": filter(lambda i: i % 2 != 0, [1, 1.2323, 2, 22.22]),
            "map": map(lambda i: i / 3, range(10)),
        },
    }
    obj_rounded = r.round_object(obj, 1, use_copy=True)
    # filter test changed !
    assert list(obj_rounded["dict"]["filter"]) == [1, 1.2, 22.2]
    assert list(obj_rounded["dict"]["map"]) == [
        0.0,
        0.3,
        0.7,
        1.0,
        1.3,
        1.7,
        2.0,
        2.3,
        2.7,
        3.0,
    ]
    assert len(list(obj["dict"]["map"])) == 10


def test_no_copy_complex_object_with_map():
    obj = {
        "list": [1.122, 55.55554, 234.3],
        "float": 1.11122156,
        "int": 1212,
        "dict": {
            "filter": filter(lambda i: i % 2 != 0, [1, 1.2323, 2, 22.22]),
            "map": map(lambda i: i / 3, range(10)),
        },
    }
    obj_rounded = r.round_object(obj, 1, use_copy=False)

    assert list(obj_rounded["dict"]["filter"]) == [1, 1.2, 22.2]
    assert list(obj_rounded["dict"]["map"]) == [
        0.0,
        0.3,
        0.7,
        1.0,
        1.3,
        1.7,
        2.0,
        2.3,
        2.7,
        3.0,
    ]
    assert len(list(obj["dict"]["map"])) == 0


def test_int_from_signif():
    assert isinstance(r.signif(12.2, 2), float)
    assert isinstance(r.signif(1222222, 3), int)

    x = [
        {"x": 2, "y": 45.556},
        (
            175,
            1222.3,
        ),
        2,
    ]
    assert isinstance(x[0]["x"], int)
    assert isinstance(x[2], int)

    x_rounded = r.signif_object(x)
    assert isinstance(x_rounded[0]["x"], int)
    assert isinstance(x_rounded[2], int)


def test_int_return():
    assert isinstance(r.round_object(10), int)
    assert isinstance(r.ceil_object(10.234234), int)
    assert isinstance(r.floor_object(10.234234), int)
