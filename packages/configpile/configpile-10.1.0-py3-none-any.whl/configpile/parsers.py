"""
Argument value parsing

This module is mostly self-contained, and provides ways to construct :class:`.Parser` instances
which parse string arguments into values.

During the configuration building, the parsed values are collected by a
:class:`configpile.collector.Collector` instance.

.. rubric:: Types

This module uses the following types.

.. py:data:: _Value

    Value being parsed by a :class:`.Parser`

.. py:data:: _Parameter

    Type received by a mapping function

.. py:data:: _ReturnType

    Type returned by a mapping function

.. py:data:: _Item

    Item in a sequence
"""

from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Callable,
    Generic,
    Iterable,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import Protocol, runtime_checkable

from .enums import ForceCase
from .userr import Err, Res, collect_seq
from .util import assert_never

if TYPE_CHECKING:
    try:
        import parsy
    except ImportError:
        pass

# those types are documented in the module docstring

_I = TypeVar("_I")  # type used only internally

_Value = TypeVar("_Value")

_Value_contra = TypeVar("_Value_contra", contravariant=True)

_Item = TypeVar("_Item")

_Parameter = TypeVar("_Parameter")

_ReturnType = TypeVar("_ReturnType")


@runtime_checkable
class Predicate(Protocol, Generic[_Value_contra]):
    """
    Defines a function or callable that takes a value and returns whether it is valid
    """

    def __call__(self, value: _Value_contra) -> bool:
        """
        Checks whether the given value is valid

        Args:
            value: Value to check

        Returns:
            True if the value is valid, False otherwise
        """


@runtime_checkable
class ErrorMessageProvider(Protocol, Generic[_Value_contra]):
    """
    Generates formatted error messages when values are invalid
    """

    def __call__(self, string_to_parse: str, parsed_value: _Value_contra) -> str:
        """
        Returns a formatted error message describing a validation problem

        Args:
            string_to_parse: String provided by the user
            parsed_value: Value parsed from string
        """


class Parser(ABC, Generic[_Value]):
    """Describes a parser, that takes a string and returns either a value or an error"""

    @abstractmethod
    def parse(self, arg: str) -> Res[_Value]:
        """
        Parses a string into a result

        This method reports parsing errors using a result type instead of raising
        exceptions.

        Example:
            >>> user_input = "invalid"
            >>> float_parser.parse(user_input)
            Err1(msg="...", contexts=[])
            >>> user_input = 2.0
            >>> float_parser.parse(user_input)
            2.0

        Args:
            arg: String value to parse

        Returns:
            A result containing either the parsed value or a description of an error
        """

    def choices(self) -> Optional[Sequence[str]]:
        """
        Returns, when relevant, a set of inputs whose parse results cover all possible values

        The definition above is written carefully: parsers may parse aliases, or normalize input
        when parsing (by stripping whitespace or normalizing case).

        This method returns a set of strings, which does not need to be minimal, so that
        their parsed values cover the set of possible result values.
        """
        return None

    def map(self, f: Callable[[_Value], _Item]) -> Parser[_Item]:
        """
        Maps successful results of the parser through the given function

        Args:
            f: Function to map the result through

        Returns:
            Updated parser
        """
        return _Mapped(self, f)

    def flat_map(self, f: Callable[[_Value], Res[_Item]]) -> Parser[_Item]:
        """
        Maps successful results of the parser through the given function that may fail

        Args:
            f: Function to map the result through, may return an error

        Returns:
            Updated parser
        """
        return _FlatMapped(self, f)

    def as_sequence_of_one(self) -> Parser[Sequence[_Value]]:
        """
        Returns a parser, that returns a sequence of a single value on success

        Returns:
            Updated parser
        """
        f: Callable[[_I], Sequence[_I]] = lambda t: [t]
        return self.map(f)

    def empty_means_none(self, strip: bool = True) -> Parser[Optional[_Value]]:
        """
        Returns a new parser where the empty string means None

        Args:
            strip: Whether to strip whitespace

        Returns:
            A new parser
        """
        return _EmptyMeansNone(self, strip)

    def separated_by(
        self, sep: str, strip: bool = True, remove_empty: bool = True
    ) -> Parser[Sequence[_Value]]:
        """
        Returns a new parser that parses values separated by a string

        Args:
            sep: Separator
            strip: Whether to strip whitespace from separated values
            remove_empty: Whether to remove empty strings before parsing them

        Returns:
            A new parser
        """
        return _SeparatedBy(self, sep, strip, remove_empty)

    def validated(
        self, predicate: Callable[[_Value], bool], msg: Union[str, Callable[[str, _Value], str]]
    ) -> _Validated[_Value]:
        """
        Returns a parser that verifies a predicate after successful parse

        Args:
            predicate: Predicate to check
            msg: Either a string, or a function that constructs a string from the parsed string
                 and the result

        Returns:
            A new parser
        """
        if isinstance(msg, str):
            c: str = msg
            assert isinstance(predicate, Predicate)
            return _Validated(self, predicate, lambda a, t: c)
        else:
            assert isinstance(predicate, Predicate)
            return _Validated(
                self,
                predicate,
                msg,
            )

    @staticmethod
    def from_parsy_parser(parser: parsy.Parser) -> Parser[_Value]:
        """
        Creates a parser from a parsy parser

        Args:
            parser: Parser returning a value of type ``t``

        Returns:
            Parameter type
        """
        import parsy  # pylint: disable=import-outside-toplevel,redefined-outer-name

        @dataclass(frozen=True)
        class _Parsy(Parser[_Value]):
            """
            Wraps a parser from the parsy library
            """

            parser: parsy.Parser

            def parse(self, arg: str) -> Res[_Value]:
                res = (self.parser << parsy.eof)(arg, 0)  # Inspired by Parser.parse
                if res.status:
                    return cast(_Value, res.value)
                else:
                    if res.furthest is not None:
                        return Err.make(
                            f"Parse error '{res.expected}' in '{arg}' at position '{res.furthest}'"
                        )
                    else:
                        return Err.make(f"Parse error '{res.expected}' in '{arg}'")

        return _Parsy(parser)

    @staticmethod
    def from_function_that_raises(
        f: Callable[[str], _Value], *catch: Type[Exception]
    ) -> Parser[_Value]:
        """
        Creates a parser from a function that raises exceptions on parse errors

        Args:
            f: Function that parses the string
            catch: Exception types to catch; if no types are provided, all exceptions will be
                   caught

        Returns:
            Parameter type
        """
        return _FromFunctionThatRaises(f, catch)

    @staticmethod
    def from_function(f: Callable[[str], Res[_Value]]) -> Parser[_Value]:
        """
        Creates a parser from a function that returns a value or an error

        Args:
            f: Function that parses the string

        Returns:
            Parameter type
        """

        return _FromFunction(f)

    @staticmethod
    def from_choices(
        values: Iterable[str],
        strip: bool = True,
        force_case: ForceCase = ForceCase.NO_CHANGE,
    ) -> Parser[str]:
        """
        Creates a parser whose values are chosen from a set of strings

        Args:
            values: Set of values
            strip: Whether to strip whitespace before looking for choices

        Returns:
            Parameter type
        """

        return Parser.from_mapping({v: v for v in values}, strip, force_case)

    @staticmethod
    def from_mapping(
        mapping: Mapping[str, _Value],
        strip: bool = True,
        force_case: ForceCase = ForceCase.NO_CHANGE,
        aliases: Optional[Mapping[str, _Value]] = None,
    ) -> Parser[_Value]:
        """
        Creates a parser whose strings correspond to keys in a dictionary

        Args:
            mapping: Dictionary mapping strings to values
            strip: Whether to strip whitespace before looking for keys
            force_case: Whether to normalize the case of the user string
            aliases: Additional mappings not shown in help

        Returns:
            Parameter type
        """
        if aliases is None:
            aliases = {}
        return _Choices(mapping, strip, force_case, aliases)


@dataclass(frozen=True)
class _Choices(Parser[_Value]):
    """
    Describes a multiple choice parser
    """

    mapping: Mapping[str, _Value]
    strip: bool
    force_case: ForceCase
    aliases: Mapping[str, _Value]

    def parse(self, arg: str) -> Res[_Value]:
        if self.strip:
            arg = arg.strip()
        if self.force_case is ForceCase.LOWER:
            arg = arg.lower()
        elif self.force_case is ForceCase.UPPER:
            arg = arg.upper()
        elif self.force_case is ForceCase.NO_CHANGE:
            pass
        else:
            assert_never(self.force_case)
        all_mappings = {**self.mapping, **self.aliases}
        if arg in all_mappings:
            return all_mappings[arg]
        else:
            msg = f"Value {arg} not in choices {','.join(self.mapping.keys())}"
            return Err.make(msg)

    def choices(self) -> Optional[Sequence[str]]:
        return list(self.mapping.keys())


@dataclass  # not frozen because mypy bug, please be responsible
class _FromFunctionThatRaises(Parser[_Value]):
    """
    Wraps a function that may raise exceptions
    """

    # the optional is to make mypy happy
    fun: Callable[[str], _Value]  #: Callable function that may raise
    catch: Sequence[Type[Exception]]

    def parse(self, arg: str) -> Res[_Value]:
        try:
            f = self.fun
            assert f is not None
            return f(arg)
        except Exception as e:  # pylint: disable=broad-except
            if (not self.catch) or any([isinstance(e, t) for t in self.catch]):
                return Err.make(f"Error '{e}' in '{arg}'")
            else:
                raise


@dataclass  # not frozen because mypy bug, please be responsible
class _FromFunction(Parser[_Value]):
    """
    Wraps a function that returns a result
    """

    fun: Callable[[str], Res[_Value]]

    def parse(self, arg: str) -> Res[_Value]:
        return self.fun(arg)


@dataclass(frozen=True)
class _EmptyMeansNone(Parser[Optional[_Item]]):
    """
    Wraps an existing parser so that "empty means none"
    """

    wrapped: Parser[_Item]  #: Wrapped Parser called if value is not empty
    strip: bool  #:  Whether to strip whitespace before testing for empty

    def parse(self, arg: str) -> Res[Optional[_Item]]:
        if self.strip:
            arg = arg.strip()
        if not arg:
            return None
        else:
            return self.wrapped.parse(arg)


@dataclass(frozen=True)
class _FlatMapped(Parser[_ReturnType], Generic[_Parameter, _ReturnType]):
    """
    Wraps an existing parser and applies a function to its successful result
    """

    wrapped: Parser[_Parameter]  #: Wrapped parser

    #: Mapping function, made optional as a hack
    f: Optional[Callable[[_Parameter], Res[_ReturnType]]]

    def parse(self, arg: str) -> Res[_ReturnType]:
        assert self.f is not None
        res: Res[_Parameter] = self.wrapped.parse(arg)
        if isinstance(res, Err):
            return res
        return self.f(res)

    def choices(self) -> Optional[Sequence[str]]:
        return self.wrapped.choices()


@dataclass(frozen=True)
class _Mapped(Parser[_ReturnType], Generic[_Parameter, _ReturnType]):
    """
    Wraps an existing parser and applies a function to its successful result
    """

    wrapped: Parser[_Parameter]  #: Wrapped parser
    f: Optional[Callable[[_Parameter], _ReturnType]]  #: Mapping function, made optional as a hack

    def parse(self, arg: str) -> Res[_ReturnType]:
        assert self.f is not None
        res: Res[_Parameter] = self.wrapped.parse(arg)
        if isinstance(res, Err):
            return res
        return self.f(res)

    def choices(self) -> Optional[Sequence[str]]:
        return self.wrapped.choices()


@dataclass(frozen=True)
class _SeparatedBy(Parser[Sequence[_Item]]):
    """
    Parses values separated by a given separator
    """

    item: Parser[_Item]  #: Parser of individual items
    sep: str  #: Item separator
    strip: bool  #: Whether to strip whitespace around separated strings
    remove_empty: bool  #: Whether to prune empty strings

    def parse(self, arg: str) -> Res[Sequence[_Item]]:
        items: Iterable[str] = arg.split(self.sep)
        if self.strip:
            items = map(lambda s: s.strip(), items)
        if self.remove_empty:
            items = filter(None, items)
        res: Sequence[Res[_Item]] = [self.item.parse(s) for s in items]

        return collect_seq(res)


@dataclass(frozen=True)
class _Validated(Parser[_Value]):
    """
    Parses a value and validates it
    """

    wrapped: Parser[_Value]
    predicate: Predicate[_Value]
    msg: ErrorMessageProvider[_Value]

    def parse(self, arg: str) -> Res[_Value]:
        res = self.wrapped.parse(arg)
        if isinstance(res, Err):
            return res
        p = self.predicate
        if p(res):
            return res
        return Err.make(self.msg(arg, res))

    def choices(self) -> Optional[Sequence[str]]:
        return self.wrapped.choices()


#: Parses a path
path_parser: Parser[pathlib.Path] = Parser.from_function_that_raises(pathlib.Path)

#: Parses an integer
int_parser: Parser[int] = Parser.from_function_that_raises(int)

#: Parses a string, preserves whitespace
str_parser: Parser[str] = Parser.from_function(lambda s: s)

#: Parses a string, stripping whitespace left and right
stripped_str_parser: Parser[str] = Parser.from_function(lambda s: s.strip())

#: Parses a float
float_parser: Parser[float] = Parser.from_function_that_raises(float)

bool_parser: Parser[bool] = Parser.from_mapping(
    {"true": True, "false": False},
    force_case=ForceCase.LOWER,
    aliases={"t": True, "f": False, "1": True, "0": False},
)
