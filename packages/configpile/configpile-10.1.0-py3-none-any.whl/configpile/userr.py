"""
Error-reporting module

This implements a union-based result type similar to `<https://github.com/rustedpy/result/>`_,
except that we do not wrap the "good" result.

The type :data:`.Res` contains either a value of a user-defined type :data:`._Value_co`, an error
or a list of errors.

Errors have an associated context, see the description for :class:`.Err1`.

.. rubric:: Types

.. py:data:: Res

    Result type (parameterized :data:`.Res` [ :data:`._Value_co` ] )

    Note:
        Wrapping an error in :data:`.Res` as in :data:`.Res` [ :class:`.Err` ] is meaningless,
        and will not do what you expect.

        There are other "monadic" result types for Python that have better composability.

    :data:`.Res` = :data:`~typing.Union` [ :data:`._Value_co`, :class:`Err` ]

.. py:data:: _Value_co

    OK Value in our custom result type

.. py:data:: _Parameters

    Parameter specification for a decorated function

.. py:data:: _ReturnType

    Return type for a decorated function

.. py:data:: _U

    Generic type

.. py:data:: _V

    Generic type

.. py:data:: _W

    Generic type

"""

from __future__ import annotations

import shutil
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    Hashable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from typing_extensions import ParamSpec


class Err(ABC):
    """
    Describes either an error or a list of errors
    """

    @abstractmethod
    def markdown(self) -> Sequence[str]:
        """
        Returns a Markdown-formatted summary of this error (or list of errors)
        """

    @abstractmethod
    def errors(self) -> Sequence[Err1]:
        """
        Returns a sequence of all contained errors

        If this is not a collection of errors :class:`.ManyErr`, returns a sequence with
        a single item, this instance itself.
        """

    @abstractmethod
    def in_context(self, **contexts: Any) -> Err:
        """
        Adds to this error information about the context in which it occurred

        Args:
            contexts: Contexts (given as key/value pairs) to append to the context list

        Returns:
            Updated error
        """

    def pretty_print(self) -> None:
        """
        Pretty prints an error on the console
        """
        try:
            from rich.console import Console  # pylint: disable=import-outside-toplevel
            from rich.markdown import Markdown  # pylint: disable=import-outside-toplevel

            console = Console()
            md = Markdown("\n".join(self.markdown()))
            console.print(md)
        except ImportError:
            sz = shutil.get_terminal_size()
            t = self.markdown()
            print(textwrap.fill("\n".join(t), width=sz.columns))

    @staticmethod
    def collect1(first_error: Err, *additional_errors: Err) -> Err:
        """
        Collect a non-empty sequence of errors into a single error

        Example:
            We can also collect errors coming from a list using the following syntax

            >>> errors = [Err.make('err 1'), Err.make('err 2'), Err.make('err 3')]
            >>> Err.collect1(*errors)
            ManyErr(errs=...)

        Args:
            first_error: First error to collect
            additional_errors: Errors to collect into a single error, at least one must be provided

        Raises:
            ValueError: If no error is provided

        Returns:
            A consolidated error
        """
        res = Err.collect(first_error, *additional_errors)
        if res is None:
            raise ValueError("Result cannot be None if at least one error is provided")
        return res

    @staticmethod
    def collect(*errs: Optional[Err]) -> Optional[Err]:
        """
        Collect a possibly empty sequence of (optional) errors into an optional single error

        Args:
            errs: (Optional) errors

        Returns:
            An error or `None`
        """

        lst: List[Err1] = []
        for e in errs:
            if e is not None:
                lst.extend(e.errors())
        if not lst:
            return None
        elif len(lst) == 1:
            return lst[0]
        else:
            return ManyErr(lst)

    @staticmethod
    def make(msg: str, **contexts: Any) -> Err1:
        """
        Creates a single error

        Example:
            >>> Err.make("test error")
            Err1(msg='test error', contexts=[])

        Args:
            msg: Error message
            contexts: Contexts (given as key/value pairs) to append to the context list

        Returns:
            An error
        """
        return Err1(msg, [*contexts.items()])

    @staticmethod
    def check(predicate: bool, msg: str, **contexts: Any) -> Optional[Err1]:
        """
        Returns an error if the given predicate is false, otherwise returns None.

        Example:
            >>> a = -1
            >>> b = 2
            >>> Err.collect(Err.check(a >= 0, "a < 0"), Err.check(b >= 0, "b < 0"))
            Err1(msg='a < 0', contexts=[])

        Args:
            predicate: Predicate to check
            msg: Error message
            contexts: Contexts (given as key/value pairs) to append to the context list

        Returns:
            An error or `None`
        """
        if predicate:
            return None
        else:
            return Err.make(msg, **contexts)


@dataclass(frozen=True)
class Err1(Err):
    """
    Describes a single error

    This error stores a sequence of contexts, which are key/value pairs describing in which
    context the error occurred. Contexts are used for explaining to the user where the error
    occurred. They shouldn't be used, in principle, to wrap additional information about the error.
    """

    msg: str  #: Error message
    contexts: Sequence[Tuple[str, Any]]  #: Contexts in which the error appears, from old to new

    def errors(self) -> Sequence[Err1]:
        return [self]

    def markdown(self, include_contexts: bool = True) -> Sequence[str]:
        c: List[str] = []
        if include_contexts:
            c = [
                line
                for (name, value) in reversed(self.contexts)
                for line in [f"In {name}: {value}", ""]
            ]
        return [*c, "`" + self.msg + "`"]

    def in_context(self, **contexts: Any) -> Err1:
        return Err1(self.msg, [*contexts.items(), *self.contexts])


@dataclass(frozen=True)
class _GroupedErrors:
    """
    Used to group errors by context when pretty-printing

    Forms a tree structure: at a level of the tree, errors which share a similar "top" context
    are grouped; other errors are kept in an ungrouped list.

    At the next level, the top-level context is popped, and the process repeat.
    """

    groups: Mapping[Tuple[str, Any], _GroupedErrors]  #: Errors grouped by context
    ungrouped: Sequence[Err1]  #: Errors not grouped by context

    def markdown(
        self,
        skip_contexts: int = 0,
    ) -> Sequence[str]:
        """
        Returns the markdown formatted info about this group of errors

        Args:
            skip_contexts: How many context to skip because they are displayed by the surrounding
                           text
        """
        lines: List[str] = []
        for ctx, ge in self.groups.items():
            ctx_name, ctx_value = ctx
            lines.append(f"* In {ctx_name}: {ctx_value}")
            lines.append("")
            lines.extend(["  " + l for l in ge.markdown(skip_contexts + 1)])
        d = len(str(len(self.ungrouped) - 1)) + 1
        for i, e in enumerate(self.ungrouped):
            err_lines: List[str] = []
            ctxs = list(e.contexts)[skip_contexts:]
            for ctx in ctxs:
                ctx_name, ctx_value = ctx
                err_lines.append(f"In {ctx_name}: {ctx_value}")
                err_lines.append("")
            err_lines.extend(e.markdown(include_contexts=False))
            num = str(i) + "." + " " * (d - len(str(i)))
            lines.append(num + err_lines[0])
            sp = " " * (d + 1)
            lines.extend([sp + l for l in err_lines[1:]])
            lines.append("")
        return lines

    @staticmethod
    def make(errors: Sequence[Err1], index: int = 0) -> _GroupedErrors:
        """
        Constructs a tree of grouped errors

        Args:
            errors: Sequence of errors
            index: Number of contexts to skip, which have already been processed
        """
        grouped_pairs: Dict[Tuple[str, Any], List[Tuple[int, Err1]]] = {}
        ungrouped_pairs: List[Tuple[int, Err1]] = []
        for i, e in enumerate(errors):
            if index < len(e.contexts):
                ctx = e.contexts[index]
                if isinstance(ctx, Hashable):
                    if ctx not in grouped_pairs:
                        grouped_pairs[ctx] = [(i, e)]
                    else:
                        grouped_pairs[ctx].append((i, e))
            else:
                ungrouped_pairs.append((i, e))
        groups: Dict[Tuple[str, Any], _GroupedErrors] = {}
        for k, v in grouped_pairs.items():
            if len(v) == 1:
                ungrouped_pairs.append((v[0]))
            else:
                groups[k] = _GroupedErrors.make([e for _, e in v], index + 1)

        def get_index(pair: Tuple[int, Err1]) -> int:
            return pair[0]

        ungrouped: List[Err1] = [e for _, e in sorted(ungrouped_pairs, key=get_index)]

        return _GroupedErrors(groups, ungrouped)


@dataclass(frozen=True)
class ManyErr(Err):
    """
    Error class that regroups several errors

    It must contain at least one error, and it makes sense to use it when there is more than one
    error present.

    This class has special support for pretty-printing a list of errors.
    """

    errs: Sequence[Err1]  #: Contained errors

    def __post_init__(self) -> None:
        assert len(self.errs) > 0, "A ManyErr should contain at least one error"
        assert all([not isinstance(e, ManyErr) for e in self.errs])

    def markdown(self) -> Sequence[str]:
        return _GroupedErrors.make(self.errs).markdown()

    def errors(self) -> Sequence[Err1]:
        return self.errs

    def in_context(self, **contexts: Any) -> Err:
        return ManyErr([e.in_context(**contexts) for e in self.errs])


# those attributes are documented in the module docstring

_U = TypeVar("_U")

_V = TypeVar("_V")

_W = TypeVar("_W")

_Value_co = TypeVar("_Value_co", covariant=True)

_Parameters = ParamSpec("_Parameters")

_ReturnType = TypeVar("_ReturnType")

Res = Union[_Value_co, Err]


def wrap(
    *keep: Type[Exception],
) -> Callable[[Callable[_Parameters, _ReturnType]], Callable[_Parameters, Res[_ReturnType]],]:
    """
    Decorates the given function, and wraps thrown exceptions into an error result

    Exception types can be provided as arguments to filter the exceptions being transformed
    into errors.

    Example:
        >>> @wrap(ValueError)
        ... def parse(s: str) -> int:
        ...     return int(s)
        >>> parse("2")
        2
        >>> parse("should error")
        Err1(msg="...", contexts=[])
    """

    def decorator(
        func: Callable[_Parameters, _ReturnType]
    ) -> Callable[_Parameters, Res[_ReturnType]]:
        def wrapper(*args, **kwargs) -> Res[_ReturnType]:  # type: ignore
            try:
                res: Res[_ReturnType] = func(*args, **kwargs)  # type: ignore
            except Exception as e:  # pylint: disable=broad-except
                if (not keep) or any([isinstance(e, t) for t in keep]):
                    res = Err.make(f"{type(e).__name__} thrown: {e}")
                else:
                    raise
            return res

        return wrapper  # type: ignore

    return decorator


@overload
def in_context(result: Optional[Err], **contexts: Any) -> Optional[Err]:
    pass


@overload
def in_context(result: Res[_Value_co], **contexts: Any) -> Res[_Value_co]:
    pass


def in_context(
    result: Union[_Value_co, Err, None], **contexts: Any
) -> Union[_Value_co, Err, None]:
    """
    Adds context to an error contained in a result type (when applicable)

    This function has different signatures depending on the argument types.

    Args:
        result: Result to enrich, if it contains an error
        contexts: Contexts to add, given as keyword arguments

    :type result: See signatures

    Returns:
        Updated result with added context

    :rtype: See signatures

    See also:
        :meth:`.Err.in_context`
    """
    if isinstance(result, Err):
        return result.in_context(**contexts)
    else:
        return result


@overload
def collect(t: Res[_Value_co], u: Res[_U]) -> Res[Tuple[_Value_co, _U]]:
    pass


@overload
def collect(t: Res[_Value_co], u: Res[_U], v: Res[_V]) -> Res[Tuple[_Value_co, _U, _V]]:
    pass


@overload
def collect(
    t: Res[_Value_co], u: Res[_U], v: Res[_V], w: Res[_W]
) -> Res[Tuple[_Value_co, _U, _V, _W]]:
    pass


def collect(*args):  # type: ignore[no-untyped-def]
    """
    Collects single results of various types into a tuple result


    :rtype: See signatures
    """
    ok: List[Any] = []
    errs: List[Err1] = []
    for arg in args:
        if isinstance(arg, Err):
            errs.extend(arg.errors())
        else:
            ok.append(arg)
    if errs:
        return Err.collect1(*errs)  # pylint: disable=no-value-for-parameter
    else:
        return tuple(ok)


def map(  # pylint: disable=redefined-builtin
    f: Callable[[_Value_co], _ReturnType], r: Res[_Value_co]
) -> Res[_ReturnType]:
    """
    Enables a computation on the value of a result

    Example:

        >>> from math import sqrt
        >>> @wrap(ValueError)
        ... def parse(s: str) -> float:
        ...    return float(s)
        >>> @wrap(ValueError)
        ... def square(f: float) -> float:
        ...    return f*f
        >>> map(square, parse("2"))
        4.0
        >>> map(square, parse("-1"))
        1.0
        >>> flat_map(square, parse("invalid"))
        Err1(msg="ValueError thrown: could not convert string to float: 'invalid'", contexts=[])

    Args:
        f: Function that takes a value of type `._Value_co` and returns a value of type
           `._ReturnType`
        r: Result parameterized by type `._Value_co`

    Returns:
        Result parameterized by type `._ReturnType`

    See also:
        :func:`.flatMap`
    """
    if isinstance(r, Err):
        return r
    else:
        return f(r)


def flat_map(f: Callable[[_Value_co], Res[_ReturnType]], r: Res[_Value_co]) -> Res[_ReturnType]:
    """
    Enables the chaining computations that can error

    Example:

        >>> from math import sqrt
        >>> @wrap(ValueError)
        ... def parse(s: str) -> float:
        ...    return float(s)
        >>> @wrap(ValueError)
        ... def my_sqrt(f: float) -> float:
        ...    return sqrt(f)
        >>> flat_map(my_sqrt, parse("2"))
        1.414...
        >>> flat_map(my_sqrt, parse("-1"))
        Err1(msg='ValueError thrown: math domain error', contexts=[])
        >>> flat_map(my_sqrt, parse("invalid"))
        Err1(msg="ValueError thrown: could not convert string to float: 'invalid'", contexts=[])

    Args:
        f: Function that takes a result parameterized by type `_Value` and returns a result
           parameterized by type `_ReturnType`
        r: Result parameterized by type `_Value`

    Returns:
        Result parameterized by type `_ReturnType`

    See also:
        :func:`.map`
    """
    if isinstance(r, Err):
        return r
    else:
        return f(r)


def collect_seq(seq: Sequence[Res[_Value_co]]) -> Res[Sequence[_Value_co]]:
    """
    Collects a sequence of results

    If any of the sequence elements is an error, the result is an error which collects all
    the errors present in the sequence.

    If all the sequence elements are values, it returns a sequence of values.

    Example:

        >>> @wrap(ValueError)
        ... def parse(s: str) -> int:
        ...    return int(s)
        >>> collect_seq([parse("2"), parse("invalid")])
        Err1(...)
        >>> collect_seq([parse("2"), parse("3")])
        [2, 3]


    Args:
        seq: Sequence of results

    Returns:
        An error or a sequence
    """
    ok: List[_Value_co] = []
    errs: List[Err1] = []
    for res in seq:
        if isinstance(res, Err):
            errs.extend(res.errors())
        else:
            ok.append(res)
    if errs:
        return Err.collect1(*errs)  # pylint: disable=unused-import
    else:
        return ok
