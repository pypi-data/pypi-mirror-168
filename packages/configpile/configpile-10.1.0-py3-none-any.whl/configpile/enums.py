"""
This module defines enumerations that are used by the library.

We collect them in this module to solve the circular import problem.
"""

from enum import Enum


class Derived(Enum):
    """
    Describes automatic handling of an argument name
    """

    #: Derives the name/key using snake_case
    SNAKE_CASE = 1

    #: Derives the name/key using SNAKE_CASE (and sets uppercase, default for env. variables)
    SNAKE_CASE_UPPER_CASE = 2

    #: Derives the argument name using kebab-case (default for INI file keys and cmd line flags)
    KEBAB_CASE = 3

    def derive(self, name: str) -> str:
        """
        Returns a derived name from a field name

        Args:
            name: Field name in Python identifier format
        """
        assert str.isidentifier(name)
        if self == Derived.SNAKE_CASE:
            return name
        elif self == Derived.SNAKE_CASE_UPPER_CASE:
            return name.upper()
        elif self == Derived.KEBAB_CASE:
            return name.replace("_", "-")
        else:
            raise NotImplementedError


class ForceCase(Enum):
    """
    Describes whether a string is normalized to lower or upper case before processing
    """

    NO_CHANGE = 0  #: Keep case
    UPPER = 1  #: Change to uppercase
    LOWER = 2  #: Change to lowercase


class Positional(Enum):
    """
    Describes the positional behavior of a parameter
    """

    ONCE = 1  #: Eats a single positional value
    ZERO_OR_MORE = 2  #: Eats as many positional values as possible
    ONE_OR_MORE = 3  #: Eats as many positional values as possible, but at least one

    def should_be_last(self) -> bool:
        """
        Returns whether a positional parameter should be the last one
        """
        return self in {Positional.ZERO_OR_MORE, Positional.ONE_OR_MORE}


class SpecialAction(Enum):
    """
    Describes special actions that do not correspond to normal execution
    """

    HELP = "help"  #: Display a help message
    VERSION = "version"  #: Print the version number
