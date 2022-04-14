import copy
import numbers
import builtins
import math
import array


class UnpickableObjectError(Exception):
    pass


class NonNumericTypeError(Exception):
    pass


def _do(func, value, digits, use_copy):
    def convert(value):
        if isinstance(value, complex):
            # this has to be checked before the Number check,
            # as complex is a Number
            return convert(value.real) + convert(value.imag) * 1j
        if isinstance(value, numbers.Number):
            return func(value, *digits)
        if isinstance(value, list):
            value[:] = list(map(convert, value))
            return value
        if isinstance(value, (tuple, set, frozenset)):
            return type(value)(convert(list(value)))
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = convert(v)
            return value
        if isinstance(value, array.array):
            value[:] = array.array(value.typecode, convert(value.tolist()))
            return value

        return value

    if use_copy:
        try:
            value = copy.deepcopy(value)
        except TypeError:
            raise UnpickableObjectError()
    return convert(value)


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
    if not isinstance(x, numbers.Number):
        raise NonNumericTypeError(
            f"x must be a number, not '{type(x).__name__}'"
        )
    d = math.ceil(math.log10(abs(x)))
    power = digits - d
    magnitude = math.pow(10, power)
    shifted = builtins.round(x * magnitude)
    return shifted / magnitude


def round_object(value, digits=None, use_copy=False):
    """Round numbers in a Python object.

    Args:
        x (any): any Python object
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
    return _do(builtins.round, value, [digits], use_copy)


def ceil_object(value, use_copy=False):
    """Round numbers in a Python object, using the ceiling algorithm.

    This means rounding to the closest greater integer.

    Args:
        x (any): any Python object
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
    return _do(math.ceil, value, [], use_copy)


def floor_object(value, use_copy=False):
    """Round numbers in a Python object, using the floor algorithm.

    This means rounding to the closest smaller integer.

    Args:
        x (any): any Python object
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
    return _do(math.floor, value, [], use_copy)


def signif_object(value, digits=3, use_copy=False):
    """Round numbers in a Python object to requested significant digits.

    Args:
        x (any): any Python object
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
    return _do(signif, value, [digits], use_copy)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
