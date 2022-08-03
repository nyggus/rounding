import array
import builtins
import copy
import math
import types
from collections import defaultdict
from collections import deque
from collections import OrderedDict
from collections import defaultdict
from collections import Counter
from collections.abc import Mapping
from collections.abc import Set
from collections import UserList
from numbers import Number
from decimal import Decimal
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Union, TypeVar


# Type declarations
IntOrFloat = Union[int, float]

dispatch_table_store: Dict = {}


class NonNumericTypeError(Exception):
    pass


class NonCallableError(Exception):
    pass


def types_lookup(type_name: str) -> Optional[Any]:
    # helper function to get a type.
    # if type_name does not exist (because of the Python version), return None
    return getattr(types, type_name, None)


def _do(func, obj, digits, use_copy):

    if type(obj) in (float, int):
        return func(obj, *digits)

    def convert_number(obj):
        return func(obj, *digits)

    def convert_complex(obj):
        return convert(obj.real) + convert(obj.imag) * 1j

    def convert_list(obj):
        if use_copy:
            return type(obj)(map(convert, obj))
        obj[:] = list(map(convert, obj))
        return obj

    def convert_map(obj):
        if use_copy:
            obj_copy = copy.deepcopy(obj)
            return map(convert, obj_copy)
        return map(convert, obj)

    def convert_filter(obj):
        return filter(
            bool, convert_map(obj)
        )  # bool of map object is always True

    def convert_generator(obj):
        return map(convert, obj)

    def convert_namedtuple(obj):
        return obj._replace(**convert(obj._asdict()))

    def convert_dict(obj):
        if use_copy:
            return_obj = type(obj)()
        else:
            return_obj = obj
        for k, v in obj.items():
            return_obj[k] = convert(v)
        return return_obj

    def convert_array(obj):
        if use_copy:
            return array.array(obj.typecode, convert(obj.tolist()))
        obj[:] = array.array(obj.typecode, convert(obj.tolist()))
        return obj

    def convert_deque(obj):
        if use_copy:
            return type(obj)(map(convert, obj))
        for i, elem in enumerate(obj):
            obj[i] = convert(elem)
        return obj

    def convert_tuple_set_frozenset(obj):
        return type(obj)(map(convert, obj))

    def convert_rest(obj):
        if isinstance(obj, Number):
            if isinstance(obj, complex):
                return type(obj)(convert_complex(obj))
            return type(obj)(convert_number(obj))
        if isinstance(obj, (list, UserList)):
            return type(obj)(convert_list(obj))
        if isinstance(obj, tuple):
            if hasattr(obj, "_fields"):  # it's a namedtuple
                return convert_namedtuple(obj)
            return convert_tuple_set_frozenset(obj)
        if isinstance(obj, Set):
            return convert_tuple_set_frozenset(obj)
        if isinstance(obj, Mapping):
            return convert_dict(obj)
        if isinstance(obj, array.array):
            return convert_array(obj)
        if isinstance(obj, deque):
            return convert_deque(obj)
        if isinstance(obj, map):
            return convert_map(obj)
        if hasattr(obj, "__dict__"):
            # placed at the end as some of the above (derived) types
            # might have a __dict__
            if use_copy:
                obj_copy = copy.copy(obj)
                for k, v in obj_copy.__dict__.items():
                    obj_copy.__dict__[k] = convert(v)
                return obj_copy
            convert_dict(obj.__dict__)
            return obj

        return obj

    def convert(obj):
        if type(obj) in (float, int):
            return func(obj, *digits)

        return dispatch_table.get(type(obj), convert_rest)(obj)

    try:
        dispatch_table = dispatch_table_store[(func, *digits, use_copy)]
    except KeyError:
        dispatch_table = dispatch_table_store[(func, *digits, use_copy)] = {
            bool: lambda obj: func(obj, *digits),
            Decimal: lambda obj: func(obj, *digits),
            Fraction: lambda obj: func(obj, *digits),
            complex: lambda obj: convert(obj.real) + convert(obj.imag) * 1j,
            list: convert_list,
            tuple: lambda obj: tuple(map(convert, obj)),
            set: lambda obj: set(map(convert, obj)),
            frozenset: lambda obj: frozenset(map(convert, obj)),
            dict: convert_dict,
            defaultdict: convert_dict,
            OrderedDict: convert_dict,
            Counter: convert_dict,
            array.array: convert_array,
            deque: convert_deque,
            map: convert_map,
            filter: convert_filter,
            range: convert_map,
            str: lambda obj: obj,
            types_lookup("NoneType"): lambda obj: obj,
            types_lookup("GeneratorType"): convert_generator,
            types_lookup("FunctionType"): lambda obj: obj,
            types_lookup("LambdaType"): lambda obj: obj,
            types_lookup("CoroutineType"): lambda obj: obj,
            types_lookup("AsyncGeneratorType"): lambda obj: obj,
            types_lookup("CellType"): lambda obj: obj,
            types_lookup("MethodType"): lambda obj: obj,
            types_lookup("BuiltinFunctionType"): lambda obj: obj,
            types_lookup("BuiltinMethodType"): lambda obj: obj,
            types_lookup("MethodWrapperType"): lambda obj: obj,
            types_lookup("NotImplementedType"): lambda obj: obj,
            types_lookup("MethodDescriptorType"): lambda obj: obj,
            types_lookup("ClassMethodDescriptorType"): lambda obj: obj,
            types_lookup("EllipsisType"): lambda obj: obj,
            types_lookup("UnionType"): lambda obj: obj,
            types_lookup("FrameType"): lambda obj: obj,
            types_lookup("MemberDescriptorType"): lambda obj: obj,
        }

    return convert(obj)


def signif(x: IntOrFloat, digits: int) -> IntOrFloat:
    """Round number to significant digits.
    Translated from Java algorithm available on
    <a href="http://stackoverflow.com/questions/202302">Stack Overflow</a>
    Args:
        x (float, int): a value to be rounded
        digits (int, optional): number of significant digits. Defaults to 3.
    Returns:
        float or int: x rounded to significant digits
    >>> signif(1.2222, 3)
    1.22
    >>> signif(12222, 3)
    12200
    >>> signif(1, 3)
    1.0
    >>> signif(123.123123, 5)
    123.12
    >>> signif(123.123123, 3)
    123.0
    >>> signif(123.123123, 1)
    100
    """
    if x == 0:
        return 0
    if not isinstance(x, Number) or isinstance(x, complex):
        raise NonNumericTypeError(
            f"x must be a (non-complex) number, not '{type(x).__name__}'"
        )
    d = math.ceil(math.log10(abs(x)))
    power = digits - d
    magnitude = math.pow(10, power)
    shifted = builtins.round(x * magnitude)
    if x >= math.pow(10, digits):
        return type(x)(round(shifted / magnitude))
    else:
        return type(x)(shifted / magnitude)


def round_object(obj: Any, digits: int = None, use_copy: bool = False) -> Any:
    """Round numbers in a Python object.
    Args:
        obj (any): any Python object
        digits (int, optional): number of digits. Defaults to 0.
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affected inplace. In the case of
            unpickable objects, TypeError will be raised.
    Returns:
        any: the object with values rounded to requested number of digits
    >>> round_object(12.12, 1)
    12.1
    >>> round_object("string", 1)
    'string'
    >>> round_object(["Shout", "Bamalama"])
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> round_object(obj, 2)
    {'number': 12.32, 'string': 'whatever', 'list': [122.45, 0.01]}
    """
    return _do(builtins.round, obj, [digits], use_copy)


def ceil_object(obj: Any, use_copy: bool = False) -> Any:
    """Round numbers in a Python object, using the ceiling algorithm.
    This means rounding to the closest greater integer.
    Args:
        obj (any): any Python object
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affect inplace.
    Returns:
        any: the object with values ceiling-rounded to requested number
            of digits
    >>> ceil_object(12.12)
    13
    >>> ceil_object("string")
    'string'
    >>> ceil_object(["Shout", "Bamalama"])
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> ceil_object(obj)
    {'number': 13, 'string': 'whatever', 'list': [123, 1]}"""
    return _do(math.ceil, obj, [], use_copy)


def floor_object(obj: Any, use_copy: bool = False) -> Any:
    """Round numbers in a Python object, using the floor algorithm.
    This means rounding to the closest smaller integer.
    Args:
        obj (any): any Python object
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affect inplace.
    Returns:
        any: the object with values floor-rounded to requested number of
            digits
    >>> floor_object(12.12)
    12
    >>> floor_object("string")
    'string'
    >>> floor_object(["Shout", "Bamalama"])
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> floor_object(obj)
    {'number': 12, 'string': 'whatever', 'list': [122, 0]}
    """
    return _do(math.floor, obj, [], use_copy)


def signif_object(obj: Any, digits: int = 3, use_copy: bool = False):
    """Round numbers in a Python object to requested significant digits.
    Args:
        obj (any): any Python object
        digits (int, optional): number of digits.
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affect inplace.
    Returns:
        any: the object with values rounded to requested number of significant
            digits
    >>> signif_object(12.12, 3)
    12.1
    >>> signif_object(.1212, 3)
    0.121
    >>> signif_object(.00001212, 3)
    1.21e-05
    >>> signif_object(.00001219, 3)
    1.22e-05
    >>> signif_object(1212.0, 3)
    1210
    >>> signif_object("string", 1)
    'string'
    >>> signif_object(["Shout", "Bamalama"], 5)
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> signif_object(obj, 3)
    {'number': 12.3, 'string': 'whatever', 'list': [122.0, 0.01]}
    """
    return _do(signif, obj, [digits], use_copy)


def map_object(
    map_function: Callable[[IntOrFloat], IntOrFloat],
    obj: Any,
    use_copy: bool = False,
):
    """Maps recursively a Python object to a given function.
    Args:
        map_function: function that converts a number and returns a number
        obj (any): any Python object
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affect inplace.
    Returns:
        any: the object with values mapped with the given map_function
    >>> map_object(abs, -1)
    1
    >>> map_object(abs, [-2, -1, 0, 1, 2])
    [2, 1, 0, 1, 2]
    >>> round_object(
    ...     map_object(
    ...         math.sin,
    ...         {0:0, 90: math.radians(90),
    ...          180: math.radians(180),
    ...          270: math.radians(270)}
    ...     ),
    ...     3
    ... )
    {0: 0.0, 90: 1.0, 180: 0.0, 270: -1.0}
    >>> map_object(abs, "string")
    'string'
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> map_object(lambda x: signif(x**.5, 3), obj)
    {'number': 3.51, 'string': 'whatever', 'list': [11.1, 0.1]}
    """
    if not callable(map_function):
        raise NonCallableError
    return _do(map_function, obj, [], use_copy)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
