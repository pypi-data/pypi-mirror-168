"""
Configuration definition

This module defines the :class:`.Config` base class, from which all configuration derive.

.. rubric:: Types

This module uses the following types.

.. py:data:: _Config

    Configuration dataclass type being constructed

"""

from __future__ import annotations

import argparse
import inspect
import os
import sys
import typing
from abc import ABC
from dataclasses import dataclass
from pathlib import Path

from .processor import Processor, SpecialAction
from .userr import Err, Res

_Config = typing.TypeVar("_Config", bound="Config")


@dataclass(frozen=True)
class IniSection:
    """
    Describes a section of an INI file to include in the current configuration
    """

    name: str  #: Section name
    strict: bool  #: Whether all the keys must correspond to parsed arguments


@dataclass(frozen=True)
class Config(ABC):
    """
    Base class for dataclasses holding configuration data

    Example:
        .. code-block:: python

            @dataclass(frozen=True)
            class Adder(Config):
                x: Annotated[int, Param.store(types.int_)]
                y: Annotated[int, Param.store(types.int_, default_value="0")]

            res = Adder.from_command_line_(args=['x','2', 'y','3'], env={})
            res.x + res.y
    """

    # region Config: INI section processing

    #: Names of sections to parse in configuration files, with unknown keys ignored
    ini_relaxed_sections_: typing.ClassVar[typing.Sequence[str]] = ["Common", "COMMON", "common"]

    #: Names of additional sections to parse in configuration files, unknown keys error
    ini_strict_sections_: typing.ClassVar[typing.Sequence[str]] = []

    @classmethod
    def ini_sections_(cls) -> typing.Sequence[IniSection]:
        """
        Returns a sequence of INI file sections to parse

        By default, this parses first the relaxed sections and then the strict ones.

        First, try to replace the contents of :attr:`.ini_relaxed_sections_`
        and :attr:`.ini_strict_sections_`. Otherwise, override this method.
        """
        relaxed = [IniSection(name, False) for name in cls.ini_relaxed_sections_]
        strict = [IniSection(name, True) for name in cls.ini_strict_sections_]
        return relaxed + strict

    # endregion

    # region Config: general information about the program being configured

    prog_: typing.ClassVar[typing.Optional[str]] = None  #: Program name

    #: Text to display before the argument help
    #:
    #: If not present, taken from the Config subclass docstring.
    description_: typing.ClassVar[typing.Optional[str]] = None

    @classmethod
    def version_(cls) -> typing.Optional[str]:
        """
        Returns the version number of this script

        Designed to be overridden by a subclass

        Returns:
            Version number as a string
        """
        return None

    # endregion

    # region Config: environment variable processing

    #: Prefix for automatically derived environment variable names
    env_prefix_: typing.ClassVar[str] = ""

    # endregion

    # region Config: information constructed by configpile

    @classmethod
    def validators_(cls: typing.Type[_Config]) -> typing.Sequence[typing.Callable[[_Config], typing.Optional[Err]]]:
        """
        Returns all validators present in the given subclass of this class

        Validators are methods that take no arguments (except self) and return an optional error.
        Their name starts with ``validate_``.

        Returns:
            A sequence of all validators
        """
        res: typing.List[typing.Callable[[_Config], typing.Optional[Err]]] = []
        for name, _ in inspect.getmembers(cls, inspect.isroutine):
            if name.startswith("validate_"):
                res.append(getattr(cls, name))
        return res

    @classmethod
    def processor_(cls: typing.Type[_Config]) -> Processor[_Config]:
        """
        Returns a processor for this configuration
        """
        return Processor.make(cls)

    # endregion

    # region Config: configuration construction

    @classmethod
    def parse_ini_contents_(cls: typing.Type[_Config], ini_contents: str) -> Res[_Config]:
        """
        Parses the contents of an INI file into a configuration

        This method skips the processing of environment variables and command-line parameters.

        Args:
            ini_contents: Multiline string describing the configuration contents

        Returns:
            A parsed configuration or an error
        """
        processor = cls.processor_()
        return processor.process_ini_contents(ini_contents)

    @classmethod
    def parse_ini_file_(cls: typing.Type[_Config], ini_file_path: Path) -> Res[_Config]:
        """
        Parses an INI file into a configuration

        This method skips the processing of environment variables and command-line parameters.

        Args:
            ini_file_path: Path to an INI file

        Returns:
            A parsed configuration or an error
        """
        processor = cls.processor_()
        return processor.process_ini_file(ini_file_path)

    @classmethod
    def parse_command_line_(
        cls: typing.Type[_Config],
        cwd: typing.Optional[Path] = None,
        args: typing.Optional[typing.Sequence[str]] = None,
        env: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> Res[typing.Union[_Config, SpecialAction]]:
        """
        Parses multiple information sources, returns a configuration, a command or an error

        Default values are taken from the current working directory, the script command line
        arguments, and the current environment variables.

        Args:
            cwd: Directory used as a base for the configuration file relative paths
            args: Command line arguments
            env: Environment variables

        Returns:
            A parsed configuration or an error
        """
        if cwd is None:
            cwd = Path.cwd()
        if args is None:
            args = sys.argv[1:]
        if env is None:
            env = os.environ
        processor = cls.processor_()
        return processor.process_command_line(cwd, args, env)

    @classmethod
    def from_command_line_(
        cls: typing.Type[_Config],
        cwd: typing.Optional[Path] = None,
        args: typing.Optional[typing.Sequence[str]] = None,
        env: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> _Config:
        """
        Parses multiple information sources into a configuration and display help on error

        Default values are taken from the current working directory, the script command line
        arguments, and the current environment variables.

        Args:
            cwd: Directory used as a base for the configuration file relative paths
            args: Command line arguments
            env: Environment variables

        Returns:
            A parsed configuration
        """
        if cwd is None:
            cwd = Path.cwd()
        if args is None:
            args = sys.argv[1:]
        if env is None:
            env = os.environ
        res = cls.parse_command_line_(cwd, args, env)

        if isinstance(res, cls):
            return res

        if isinstance(res, Err):
            print("Encountered errors:")
            res.pretty_print()
            print(" ")
            cls.get_argument_parser_().print_help()
            sys.exit(1)

        assert isinstance(res, SpecialAction)
        if res == SpecialAction.HELP:
            cls.processor_().argument_parser.print_help()
            sys.exit(0)
        elif res == SpecialAction.VERSION:
            v = cls.version_()
            if v is None:
                v = "Unknown version number"
            print(v)
            sys.exit(0)
        else:
            raise NotImplementedError(f"Unknown special action {res}")

    # endregion

    # region Config: argparse fallback for documentation purposes

    @classmethod
    def get_argument_parser_(cls: typing.Type[_Config]) -> argparse.ArgumentParser:
        """
        Returns an :class:`argparse.ArgumentParser` for documentation purposes

        This may be removed or deprecated in later versions of configpile, if we write our
        own help/usage display function, and propose a Sphinx extension.
        """
        return cls.processor_().argument_parser

    # endregion
