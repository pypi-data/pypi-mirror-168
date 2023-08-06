"""
This module defines the handlers that are used during processing.

.. rubric:: Types

This module uses the following types.

.. py:data:: _Value

    Value being parsed by a :class:`~configpile.parsers.Parser`
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generic, List, Mapping, Optional, Sequence, Tuple, TypeVar

from .arg import Positional
from .enums import SpecialAction
from .userr import Err, in_context

if TYPE_CHECKING:
    from .arg import Expander, Param
    from .processor import State

_Value = TypeVar("_Value")


class CLHandler(ABC):
    """
    A handler for command-line arguments
    """

    @abstractmethod
    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        """
        Processes arguments, possibly updating the state or returning errors

        Args:
            args: Command-line arguments not processed yet
            state: (Mutable) state to possibly update

        Returns:
            The updated command-line and an optional error
        """


@dataclass(frozen=True)
class CLSpecialAction(CLHandler):
    """
    A handler that sets the special action
    """

    special_action: SpecialAction  #: Special action to set

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        if state.special_action is not None:
            before = state.special_action.name
            now = self.special_action.name
            err = Err.make(f"We had already action {before}, conflicts with action {now}")
            return (args, err)
        state.special_action = self.special_action
        return (args, None)


@dataclass(frozen=True)
class CLInserter(CLHandler):
    """
    Handler that expands a flag into a sequence of args inserted into the command line to be parsed
    """

    #: Arguments inserted in the command-line
    inserted_args: Sequence[str]

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        return ([*self.inserted_args, *args], None)


@dataclass(frozen=True)
class CLParam(CLHandler, Generic[_Value]):
    """
    Parameter handler

    Takes a single string argument from the command line, parses it and pushes into the
    corresponding sequence of instances
    """

    #: Parameter to handle
    param: Param[_Value]

    def action(self, value: _Value, state: State) -> Optional[Err]:
        """
        A method called on the successful parse of a value

        Can be overridden. By default does nothing.

        Args:
            value: Parsed value
            state: State to possibly update

        Returns:
            An optional error
        """
        return None

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        if args:
            res = self.param.parser.parse(args[0])
            if isinstance(res, Err):
                return (args[1:], res.in_context(param=self.param.name))
            else:
                assert self.param.name is not None, "Names are assigned after initialization"
                err = in_context(self.action(res, state), param=self.param.name)
                state.instances[self.param.name] = [*state.instances[self.param.name], res]
                return (args[1:], err)
        else:
            return (
                args,
                Err.make("Expected value, but no argument present", param=self.param.name),
            )


@dataclass(frozen=True)
class CLRootParam(CLParam[Path]):
    """
    A root path parameter handler

    Changes the root path used to resolve configuration file relative paths
    """

    def action(self, value: Path, state: State) -> Optional[Err]:
        state.root_path = value
        return None


@dataclass(frozen=True)
class CLConfigParam(CLParam[Sequence[Path]]):
    """
    A configuration file parameter handler

    If paths are successfully parsed, it appends configuration files to be parsed to the current
    state.
    """

    def action(self, value: Sequence[Path], state: State) -> Optional[Err]:
        state.config_files_to_process.extend(value)
        return None


@dataclass
class CLPos(CLHandler):
    """
    Handles positional parameters

    Note that this handler has state, namely the positional parameters that are still expected.
    """

    pos: List[Param[Any]]  #: (Mutable) list of positional parameters

    @staticmethod
    def make(seq: Sequence[Param[Any]]) -> CLPos:
        """
        Constructs a positional parameter handler from a sequence of positional parameters

        Args:
            seq: Positional parameters

        Returns:
            Handler
        """
        assert all([p.positional is not None for p in seq]), "All parameters should be positional"
        assert all(
            [not p.positional.should_be_last() for p in seq[:-1] if p.positional is not None]
        ), "Positional parameters with a variable number of arguments should be last"
        l = list(seq)  # makes a mutable copy
        return CLPos(l)

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        if not args:
            return (args, None)  # should not happen ,but let's not crash
        if not self.pos:
            return (args[1:], Err.make(f"Unknown argument {args[0]}"))
        p = self.pos[0]
        assert p.name is not None
        res = p.parser.parse(args[0])
        if isinstance(res, Err):
            return (args[1:], in_context(res, param=p.name))
        else:
            state.append(p.name, res)
            if p.positional == Positional.ONCE:
                self.pos = self.pos[1:]
            return (args[1:], None)


@dataclass(frozen=True)
class CLStdHandler(CLHandler):
    """
    The standard command line arguments handler

    It processes arguments one by one. If it recognizes a flag, the corresponding handler is
    called. Otherwise, control is passed to the fallback handler, which by default processes
    positional parameters.
    """

    flags: Mapping[str, CLHandler]
    fallback: CLHandler

    def handle(self, args: Sequence[str], state: State) -> Tuple[Sequence[str], Optional[Err]]:
        if not args:
            return (args, None)
        flag = args[0]
        handler = self.flags.get(flag)
        if handler is not None:
            next_args, err = handler.handle(args[1:], state)
            err = in_context(err, flag=flag)
            return next_args, err
        else:
            return self.fallback.handle(args, state)


class KVHandler(ABC):
    """
    Handler for key/value pairs found for example in environment variables or INI files

    Note that the key is not stored/processed in this class.
    """

    @abstractmethod
    def handle(self, value: str, state: State) -> Optional[Err]:
        """
        Processes

        Args:
            value: Value to parse and process
            state: State to update

        Returns:
            An error if an error occurred
        """


@dataclass(frozen=True)
class KVParam(KVHandler, Generic[_Value]):
    """
    Handler for the value following a key corresponding to a parameter
    """

    #: Parameter to handle
    param: Param[_Value]

    def action(self, value: _Value, state: State) -> Optional[Err]:
        """
        A method called on the successful parse of a value

        Can be overridden. By default does nothing.

        Args:
            value: Parsed value
            state: State to possibly update

        Returns:
            An optional error
        """
        return None

    def handle(self, value: str, state: State) -> Optional[Err]:
        res = self.param.parser.parse(value)
        if isinstance(res, Err):
            return res
        else:
            assert self.param.name is not None
            err = self.action(res, state)
            state.instances[self.param.name] = [*state.instances[self.param.name], res]
            return in_context(err, param=self.param.name)


@dataclass(frozen=True)
class KVConfigParam(KVParam[Sequence[Path]]):
    """
    Handler for the configuration file value following a key corresponding to a parameter
    """

    def action(self, value: Sequence[Path], state: State) -> Optional[Err]:
        state.config_files_to_process.extend(value)
        return None


@dataclass(frozen=True)
class KVRootParam(KVParam[Path]):
    """
    A root path parameter handler

    Changes the root path used to resolve configuration file relative paths
    """

    def action(self, value: Path, state: State) -> Optional[Err]:
        state.root_path = value
        return None
