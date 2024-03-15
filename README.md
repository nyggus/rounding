# `rounder`: Rounding of numbers in complex Python objects

`rounder` is a lightweight package for rounding numbers in complex Python objects, such as dictionaries, lists, tuples, and sets, and any complex object that combines any number of such objects in any nested structure; you can also use it for instances of classes whose attributes contain numbers. The code is organized as a Python (Python >= 3.6 is required) package that can be installed from PyPi (`pip install rounder`), but as it is a one-file package, you can simply download its main module ([rounder.py](rounder/rounder.py)) and use it directly in your project.

The package is useful mainly for presentation purposes, but in some cases, it can be useful in other situations as well.

`rounder` offers you four functions for rounding objects:

* `round_object(obj, digits=0, use_copy=False)`, which rounds all numbers in `obj` to `digits` decimal places
* `floor_object(obj, use_copy=False)`, which rounds all numbers in `obj` down to the nearest integer
* `ceil_object(obj, use_copy=False)`, which rounds all numbers in `obj` up to the nearest integer
* `signif_object(obj, digits, use_copy=False)`, which rounds all numbers in `obj` to `digits` significant digits

In addition, `rounder` comes with a generalized function:

* `map_obj(func, obj, use_copy=False)`, which runs callable `func`, which takes a number as an argument and returns a number, to all numbers across the object.

`rounder` also offers a function for rounding numbers to significant digits:

* `signif(x, digits)`, which rounds `x` (either an int or a float) to `digits` significant digits

You can use `signif` in a simple way:

```python
>>> import rounder as r
>>> r.signif(1.1212, 3)
1.12
>>> r.signif(12.1239112, 5)
12.124
>>> r.signif(121212.12, 3)
121000.0

```

The package is simple to use, but you have to remember that when you're working with mutable objects, such as dicts or lists, rounding them will affect the original object; no such effect, of course, will occur for immutable types (e.g., tuples and sets). To overcome this effect, simply use `use_copy=True` in the above functions (not in `signif`). If you do so, the function will create a deep copy of the object, work on it, and return it; the original object will not be affected in any way.

You can use `rounder` functions for rounding floats, but do remember that their behavior is slightly different than that of their `builtin` and `math` counterparts, as the former, unlike the latter, do not throw an exception when a non-number object is used.

You can round, for example, a list, a tuple, a set (including a frozenset), a double `array.array`, and a dict:

```python
>>> r.round_object([1.122, 2.4434], 1)
[1.1, 2.4]
>>> r.ceil_object([1.122, 2.4434])
[2, 3]
>>> r.floor_object([1.122, 2.4434])
[1, 2]
>>> r.signif_object([1.1224, 222.4434], 4)
[1.122, 222.4]

>>> r.round_object((1.122, 2.4434), 1)
(1.1, 2.4)
>>> r.round_object({1.122, 2.4434}, 1)
{1.1, 2.4}
>>> r.round_object({"1": 1.122, "q":2.4434}, 1)
{'1': 1.1, 'q': 2.4}

>>> import array
>>> arr = array.array("d", (1.122, 2.4434))
>>> r.round_object(arr, 1)
array('d', [1.1, 2.4])

```

As mentioned above, you can use `rounder` functions also for class instances:

```python
>>> class ClassWithNumbers:
...     def __init__(self, x, y):
...         self.x = x
...         self.y = y
>>> inst = ClassWithNumbers(
...     x = 20.22045,
...     y={"list": [34.554, 666.777],
...     "tuple": (.111210, 343.3333)}
... )

>>> inst_copy = r.round_object(inst, 1, True)
>>> inst_copy.x
20.2
>>> inst_copy.y
{'list': [34.6, 666.8], 'tuple': (0.1, 343.3)}
>>> id(inst) != id(inst_copy)
True

>>> inst.x
20.22045
>>> inst_no_copy = r.floor_object(inst, False)
>>> id(inst) == id(inst_no_copy)
True
>>> inst.x
20

```

You can of course round a particular attribute of the class instance:

```python
>>> _ = r.round_object(inst_copy.y, 0, False)
>>> inst_copy.y
{'list': [35.0, 667.0], 'tuple': (0.0, 343.0)}

```

Note that you do not have to worry about having non-roundable objects in the object fed into the `rounder` functions. Your objects can contain objects of any type; numbers will be rounded while all other objects will remain untouched:

```python
>>> r.round_object([1.122, "string", 2.4434, 2.45454545-2j], 1)
[1.1, 'string', 2.4, (2.5-2j)]

```

In fact, you can round any object, and the function will simply return it if it cannot be rounded:

```python
>>> r.round_object("string")
'string'
>>> r.round_object(lambda x: x**3)(2)
8
>>> class Example: ...
>>> r.round_object(Example)
<class '__main__.Example'>
>>> r.round_object(Example())
<__main__.Example object at 0x...>

```

But most of all, you can apply rounding for any complex object, of any structure. Imagine you have a structure like this:

```python
>>> x = {
...     "items": ["item 1", "item 2", "item 3",],
...     "quantities": {"item 1": 235, "item 2" : 300, "item 3": 17,},
...     "prices": {
...         "item 1": {"$": 32.22534554, "EURO": 41.783234567},
...         "item 2": {"$": 42.26625, "EURO": 51.333578},
...         "item 3": {"$": 2.223043225, "EURO": 2.78098721346}
...     },
...     "income": {
...         "2009": {"$": 3445342.324364, "EURO":   39080.332546},
...         "2010": {"$": 6765675.56665554, "EURO": 78980.34564546},
...     }
... }

```

To round all the values in this structure, you would need to build a dedicated function. With `rounder`, this is a piece of cake:

```python
>>> rounded_x = r.round_object(x, digits=2, use_copy=True)

```

And you will get this:

```python
>>> from pprint import pprint
>>> pprint(rounded_x)
{'income': {'2009': {'$': 3445342.32, 'EURO': 39080.33},
            '2010': {'$': 6765675.57, 'EURO': 78980.35}},
 'items': ['item 1', 'item 2', 'item 3'],
 'prices': {'item 1': {'$': 32.23, 'EURO': 41.78},
            'item 2': {'$': 42.27, 'EURO': 51.33},
            'item 3': {'$': 2.22, 'EURO': 2.78}},
 'quantities': {'item 1': 235, 'item 2': 300, 'item 3': 17}}

```

Note that we used `use_copy=True`, which means that `rounded_x` is a deepcopy of `x`, so the original dictionary has not been affected anyway.


### `map_object`

In addition, `rounder` offers you a `map_object()` function, which enables you to run any function that takes a number and returns a number for all numbers in an object. This works like the following:

```python
>>> xy = {
...     "x": [12, 33.3, 45.5, 3543.22],
...     "y": [.45, .3554, .55223, .9911],
...     "expl": "x and y values"
... }
>>> r.round_object(
...     r.map_object(
...         lambda x: x**3/(1 - 1/x),
...         xy,
...         use_copy=True),
...     4,
...     use_copy=True
... )
{'x': [1885.0909, 38069.258, 96313.1475, 44495587353.9829], 'y': [-0.0746, -0.0248, -0.2077, -108.4126], 'expl': 'x and y values'}

```

You would have achieved the same result had you used `round` inside the `lambda` body:

```python
>>> r.map_object(lambda x: round(x**3/(1 - 1/x), 4), xy, use_copy=True)
{'x': [1885.0909, 38069.258, 96313.1475, 44495587353.9829], 'y': [-0.0746, -0.0248, -0.2077, -108.4126], 'expl': 'x and y values'}

```

The latter approach, actually, will be quicker, as the full recursion is used just once (by `r.map_object()`), not twice, as it was done in the former example (first, by `r.map_object()`, and then by `r.round_object()`).


If the function takes additional arguments, you can use a wrapper function to overcome this issue:

```python
>>> def forget(something): pass
>>> def fun(x, to_forget):
...     forget(to_forget)
...     return x**2
>>> def wrapper(x):
...     return fun(x, "this can be forgotten")
>>> r.map_object(wrapper, [2, 2, [3, 3, ], {"a": 5}])
[4, 4, [9, 9], {'a': 25}]

```

Or even:

```python
>>> r.map_object(
...     lambda x: fun(x, "this can be forgotten"),
...     [2, 2, [3, 3, ], {"a": 5}]
... )
[4, 4, [9, 9], {'a': 25}]

```

# Types that `rounder` works with

First of all, all these functions will work the very same way as their original counterparts (not for `signif`, which does not have one):

```python
>>> import math
>>> x = 12345.12345678901234567890
>>> for d in range(10):
...     assert round(x, d) == r.round_object(x, d)
...     assert math.ceil(x) == r.ceil_object(x)
...     assert math.floor(x) == r.floor_object(x)

```

The power of `rounder`, however, comes with working with many other types, and in particular, complex objects that contains them. `rounder` will work with the following types:

* `int`
* `float`
* `complex`
* `decimal.Decimal`
* `fractions.Fraction`
* `set` and `frozenset`
* `list`
* `tuple`
* `collections.namedtuple` and `typing.NamedTuple`
* `dict`
* `collections.defaultdict`, `collections.OrderedDict` and `collections.UserDict`
* `collections.Counter`
* `collections.deque`
* `array.array`
* `map`
* `filter`
* generators and generator functions

> Note that `rounder` will work with any type that follows the `collections.abc.Mapping` interface.

> `collections.Counter`: Beware that using `rounder` for this type will affect the _values_ of the counter, which originally represent counts. In most cases, that would mean no effect on such counts (for `rounder.round_object()`, `rounder.ceil_object()` and `rounder.floor_object()`), but `rounder.signif_object()` and `rounder.map_object()` can change the counts. In rare situations, you can keep float values as values in the counter; in such situations, `rounder` will work as expected.

> If `rounder` meets a type that is not recognized as any of the given above, it will simply return it untouched.

> "Warning": In the case of `range` objects, generators and generator functions, the `rounder` functions will change the type of the object, returning a `map` object. This should not affect the final result the using these objects, unless you directly use their types somehow.


## Immutable types

`rounder` does work with immutable types! It simply creates a new object, with rounded numbers:

```python
>>> x = {1.12, 4.555}
>>> r.round_object(x)
{1.0, 5.0}
>>> r.round_object(frozenset(x))
frozenset({1.0, 5.0})
>>> r.round_object((1.12, 4.555))
(1.0, 5.0)
>>> r.round_object(({1.1, 1.2}, frozenset({1.444, 2.222})))
({1.0}, frozenset({1.0, 2.0}))

```

So, note that it makes no difference whether you use `True` or `False` for `use_copy`, as with immutable types `rounder` will create a copy anyway.

Remember, however, that in the case of sets, you can get a shorter set then the original one:

```python
>>> x = {1.12, 1.99}
>>> r.ceil_object(x)
{2}

```


## NumPy and Pandas

`rounder` does not work with `numpy` and `pandas`: they have their own builtin methods for rounding, and using them will be much quicker. However, if for some reason a `rounder` function meets a `pandas` or a `numpy` object on its way, like here:

```python
r.round_object(dict(
    values=np.array([1.223, 3.3332, 2.323]),
    something_else="whatever else"
)

```

then it will simply return the object untouched.


# Testing

The package is covered with unit `pytest`s, located in the [tests/ folder](tests/). In addition, the package uses `doctest`s, which are collected in this README and in the main module, [rounder.py](rounder/rounder.py). These `doctest`s serve mainly documentation purposes, and since they can be run any time during development and before each release, they help to check whether all the examples are correct and work fine.


# OS

The package is OS-independent. Its releases are checked in local machines, on Windows 10 and Ubuntu 20.04 for Windows, and in Pythonista for iPad.
