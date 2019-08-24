"""
Pybars3 helpers, called from Handlebars templates.

This is a Pybars3 port of original Mozilla Handlebars.js helpers from
"ssl-config-generator/src/js/helpers".
"""
from ssl_config._versions import Version as _Version


def eq(_, item, value):
    """
    Equality.

    Args:
        _: Ignored pybars context.
        item: Item.
        value: Value.

    Returns:
        bool: True if equal.
    """
    return item == value


def includes(_, item, string_or_array):
    """
    Item is included.

    Args:
        _: Ignored pybars context.
        item (str): Item.
        string_or_array (str or iterable of str): Included in.

    Returns:
        bool: True if item is included.
    """
    return item in string_or_array


def join(_, array, joiner):
    """
    Join array.

    Args:
        _: Ignored pybars context.
        array (list): Array.
        joiner (str): Delimiter

    Returns:
        str: Joined array.
    """
    return joiner.join(array)


def last(_, some_array):
    """
    Last element of array.

    Args:
        _: Ignored pybars context.
        some_array (list): Array

    Returns:
        str: Last element.
    """
    return some_array[-1]


def minpatchver(_, minimumver, curver):
    """
    Returns true if it means the minimum patch version *and* is the same minor
    version (e.g. 2.2).

    Args:
        _: Ignored pybars context.
        minimumver (str): Minimum version.
        curver (str): Version.

    Returns:
        bool:
    """
    return sameminorver(_, minimumver, curver) and minver(_, minimumver, curver)


def minver(_, minimumver, curver):
    """
    Compare to a minimum version requirement.

    Args:
        _: Ignored pybars context.
        minimumver (str): Minimum version required. If no prerelease specified,
            is lower to any prerelease when comparing.
        curver (str): Version.

    Returns:
        bool: True if fir minimum requirement.
    """
    return _Version(curver) >= _Version(minimumver, pre=True)


def replace(_, string, what_to_replace, replacement):
    """
    Replace in string.

    Args:
        _: Ignored pybars context.
        string (str): String.
        what_to_replace (str): To replace.
        replacement (str): Replacement.

    Returns:
        str: Updated string.
    """
    return string.replace(what_to_replace, replacement)


def reverse(_, some_array):
    """
    Reverse iterable.

    Args:
        _: Ignored pybars context.
        some_array (iterable):

    Returns:
        list: reversed iterable.
    """
    return reversed(some_array)


def sameminorver(_, minorver, curver):
    """
    Return True is same minor version.

    Args:
        _: Ignored pybars context.
        minorver (str): Minor version.
        curver (str): Version.

    Returns:
        bool: True if same minor version.
    """
    min_ver = _Version(minorver)
    ver = _Version(curver)
    return min_ver.major == ver.major and min_ver.minor == ver.minor


def split(_, string, splitter):
    """
    Split string.

    Args:
        _: Ignored pybars context.
        string (str): String
        splitter (str): Delimiter.

    Returns:
        str: Updated string.
    """
    return string.split(splitter)


#: Helpers mapping to pass to Pybars.
HELPERS = {name: function for name, function in locals().items()
           if not name.startswith('_')}
