import array
import builtins
import copy
import math
from collections import defaultdict
from collections import namedtuple
from collections import deque
from collections import OrderedDict, UserDict
from collections import Counter
from collections.abc import Mapping
from numbers import Number
from typing import NamedTuple
from decimal import Decimal
from fractions import Fraction


class UnpickableObjectError(Exception):
    pass


class NonNumericTypeError(Exception):
    pass


class NonCallableError(Exception):
    pass


def _do(func, obj, digits, use_copy):
    def convert_number(obj):
        return func(obj, *digits)
        
    def convert_complex(obj):
        return convert(obj.real) + convert(obj.imag) * 1j        

    def convert_list(obj):
        obj[:] = list(map(convert, obj))
        return obj
        
    def convert_tuple(obj):
        return tuple(map(convert, obj))       
        
    def convert_set(obj):
        return set(map(convert, obj))
    
    def convert_frozenset(obj):
        return frozenset(map(convert, obj))
        
    def convert_namedtuple(obj):
        return obj._replace(**convert(obj._asdict()))                

    def convert_dict(obj):
        for k, v in obj.items():
            obj[k] = convert(obj[k])
        return obj

    def convert_array(obj):
        obj[:] = array.array(obj.typecode, convert(obj.tolist()))
        return obj

    def convert_deque(obj):
        for i, elem in enumerate(obj):
            obj[i] = convert(elem)
        return obj

    def convert_tuple_set_frozenset():
        return type(obj)(map(convert, obj))       
        
            
    def convert_rest(obj):
        try:            
            if hasattr(obj, "__dict__") and not isinstance(obj, tuple):
                # placed at the beginning to allow fast handling of class instances
                convert(obj.__dict__)
                return obj
    
            if isinstance(obj, complex):
                # this has to be checked before the Number check,
                # as complex is a Number
                return convert_complex(convert(obj))
            if isinstance(obj, Number):
                return convert_number(obj)
            if isinstance(obj, list):
                return convert_list(obj)
            if isinstance(obj, tuple):
                if hasattr(obj, "_fields"):  # it's a namedtuple
                    return convert_namedtuple(obj)
                return convert_tuple_set_frozenset(obj)
            if isinstance(obj, set, frozenset):
                return convert_tuple_set_frozenset(obj)
            if isinstance(obj, frozenset):
                return convert_frozenset(obj)
            if isinstance(obj, Mapping):
                return convert_dict(obj)
            if isinstance(obj, array.array):
                return convert_array(obj)
            if isinstance(obj, deque):
                return convert_deque(obj)
        except Exception:
            ...

        return obj

    def convert(obj):
        return dispatch_table.get(type(obj), convert_rest)(obj)

    dispatch_table = {
        float: convert_number,
        int: convert_number,
        bool: convert_number,
        Decimal: convert_number,
        Fraction: convert_number,
        complex: convert_complex,
        list: convert_list,
        tuple: convert_tuple,
        namedtuple: convert_namedtuple,
        NamedTuple: convert_namedtuple,
        set: convert_set,
        frozenset: convert_frozenset,
        dict: convert_dict,
        OrderedDict: convert_dict,
        UserDict: convert_dict,
        Counter: convert_dict,         
        defaultdict: convert_dict,
        array.array: convert_array,
        deque: convert_deque,
        str: lambda obj: obj,
    }
    if use_copy:
        try:
            obj = copy.deepcopy(obj)
        except TypeError:
            raise UnpickableObjectError()
    return convert(obj)


def signif(x, digits):
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
    12200.0
    >>> signif(1, 3)
    1.0
    >>> signif(123.123123, 5)
    123.12
    >>> signif(123.123123, 3)
    123.0
    >>> signif(123.123123, 1)
    100.0
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
    return shifted / magnitude


def round_object(obj, digits=None, use_copy=False):
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


def ceil_object(obj, use_copy=False):
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


def floor_object(obj, use_copy=False):
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


def signif_object(obj, digits=3, use_copy=False):
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
    1210.0

    >>> signif_object("string", 1)
    'string'
    >>> signif_object(["Shout", "Bamalama"], 5)
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> signif_object(obj, 3)
    {'number': 12.3, 'string': 'whatever', 'list': [122.0, 0.01]}
    """
    return _do(signif, obj, [digits], use_copy)


def map_object(map_function, obj, use_copy=False):
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
    ...         {0:0, 90: math.radians(90), 180: math.radians(180), 270: math.radians(270)}),
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
