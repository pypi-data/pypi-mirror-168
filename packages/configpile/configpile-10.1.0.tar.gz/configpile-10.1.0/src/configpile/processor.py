"""
Arguments processing

This module contains the internal machinery that processes environment variables, configuration
files and command-line parameters.

As of March 22, 2022, configpile is still pretty much influenced by :mod:`argparse`, and the
machinery below supports a subset of :mod:`argparse` functionality. Later on, we may cut ties
with :mod:`argparse`, add our own help/usage message writing, our own Sphinx extension and
encourage extending those processing classes.

.. rubric:: Types

This module uses the following types.

.. py:data:: _Config

    Type of the configuration dataclass to construct
"""

from __future__ import annotations

import argparse
import configparser
import sys
import warnings
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import Annotated, get_args, get_origin, get_type_hints

from .arg import Arg, Expander, Param
from .enums import SpecialAction
from .handlers import CLHandler, CLPos, CLSpecialAction, CLStdHandler, KVHandler
from .userr import Err, Res
from .util import ClassDoc, filter_types_single

if TYPE_CHECKING:
    from .config import Config

_Config = TypeVar("_Config", bound="Config")


@dataclass
class State:
    """
    Describes the (mutable) state of a configuration being parsed
    """

    root_path: Optional[Path]  #: Base path to use to resolve relative config file paths
    instances: Dict[str, List[Any]]  #: Contains the sequence of values for each parameter
    config_files_to_process: List[Path]  #: Contains a list of configuration files to process
    special_action: Optional[SpecialAction]  #: Contains a special action if flag was encountered

    def append(self, key: str, value: Any) -> None:
        """
        Appends a value to a parameter

        No type checking is performed, be careful.

        Args:
            key: Parameter name
            value: Value to append
        """
        assert key in self.instances, f"{key} is not a Param name"
        self.instances[key] = [*self.instances[key], value]

    @staticmethod
    def make(root_path: Optional[Path], params: Iterable[Param[Any]]) -> State:
        """
        Creates the initial state, populated with the default values when present

        Args:
            params: Sequence of parameters

        Raises:
            ValueError: If a default value cannot be parsed correctly

        Returns:
            The initial mutable state
        """
        instances: Dict[str, List[Any]] = {}

        for p in params:
            assert p.name is not None, "Arguments have names after initialization"
            if p.default_value is not None:
                res = p.parser.parse(p.default_value)
                if isinstance(res, Err):
                    raise ValueError(f"Invalid default {p.default_value} for parameter {p.name}")
                instances[p.name] = [res]
            else:
                instances[p.name] = []
        return State(root_path, instances, config_files_to_process=[], special_action=None)


@dataclass(frozen=True)
class IniProcessor:
    """
    INI configuration file processor
    """

    section_strict: Mapping[str, bool]  #: Sections and their strictness
    kv_handlers: Mapping[str, KVHandler]  #: Handler for key/value pairs

    def _process(self, parser: ConfigParser, state: State) -> Sequence[Err]:
        """
        Processes a filled ConfigParser

        Args:
            parser: INI data to parse
            state: Mutable state to update

        Returns:
            Errors that occurred, if any
        """
        errors: List[Err] = []
        try:
            for section_name in parser.sections():
                if section_name in self.section_strict:
                    for key, value in parser[section_name].items():
                        err: Optional[Err] = None
                        if key in self.kv_handlers:
                            res = self.kv_handlers[key].handle(value, state)
                            if isinstance(res, Err):
                                err = res
                        else:
                            if self.section_strict[section_name]:
                                err = Err.make(f"Unknown key {key}")
                        if err is not None:
                            errors.append(err.in_context(ini_section=section_name))
        except configparser.Error:
            errors.append(Err.make("Parse error"))
        except IOError:
            errors.append(Err.make("IO Error"))
        return errors

    def process_string(self, ini_contents: str, state: State) -> Optional[Err]:
        """
        Processes a configuration file given as a string

        Args:
            ini_contents: Contents of the INI file
            state: Mutable state to update

        Returns:
            An optional error
        """
        errors: List[Err] = []
        parser = ConfigParser()
        try:
            parser.read_string(ini_contents)
            errors.extend(self._process(parser, state))
        except configparser.Error:
            errors.append(Err.make("Parse error"))
        except IOError:
            errors.append(Err.make("IO Error"))
        if errors:
            return Err.collect(*errors)
        else:
            return None

    def process(self, ini_file_path: Path, state: State) -> Optional[Err]:
        """
        Processes a configuration file

        Args:
            ini_path: Path to the INI file
            state: Mutable state to update

        Returns:
            An optional error
        """
        errors: List[Err] = []
        if not ini_file_path.exists():
            return Err.make(f"Config file {ini_file_path} does not exist")
        if not ini_file_path.is_file():
            return Err.make(f"Path {ini_file_path} is not a file")
        parser = ConfigParser()
        # disable conversion to lower-case
        parser.optionxform = str  # type: ignore
        try:
            with open(ini_file_path, "r", encoding="utf-8") as file:
                parser.read_file(file)
                errors.extend(self._process(parser, state))
        except configparser.Error:
            errors.append(Err.make("Parse error"))
        except IOError:
            errors.append(Err.make("IO Error"))
        if errors:
            return Err.collect(*errors)
        else:
            return None


@dataclass
class ProcessorFactory(Generic[_Config]):
    """
    Describes a processor in construction

    This factory is passed to the different arguments present in the configuration.
    """

    #: List of parameters indexed by their field name
    params_by_name: Dict[str, Param[Any]]

    #: Argument parser to update, used to display help and for the Sphinx documentation
    argument_parser: argparse.ArgumentParser

    #: Argument parser group for commands
    ap_commands: argparse._ArgumentGroup

    #: Argument parser group for required parameters
    ap_required: argparse._ArgumentGroup

    #: Argument parser group for optional parameters
    ap_optional: argparse._ArgumentGroup

    #: Handlers for environment variables
    env_handlers: Dict[str, KVHandler]  # = {}

    #: List of INI sections with their corresponding strictness
    ini_section_strict: Dict[str, bool]

    #: List of handlers for key/value pairs present in INI files
    ini_handlers: Dict[str, KVHandler]

    #: List of command line flag handlers
    cl_flag_handlers: Dict[str, CLHandler]

    #: List of positional arguments
    cl_positionals: List[Param[Any]]

    validators: List[Callable[[_Config], Optional[Err]]]

    @staticmethod
    def make(config_type: Type[_Config]) -> ProcessorFactory[_Config]:
        """
        Constructs an empty processor factory

        Args:
            config_type: Configuration to process

        Returns:
            A processor factory
        """
        # fill program name from script invocation
        prog = config_type.prog_
        if prog is None:
            prog = sys.argv[0]

        # fill description from class docstring
        description: Optional[str] = config_type.description_
        if description is None:
            description = config_type.__doc__

        argument_parser = argparse.ArgumentParser(
            prog=prog,
            description=description,
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False,
        )
        argument_parser._action_groups.pop()  # pylint: disable=protected-access
        return ProcessorFactory(
            params_by_name={},
            argument_parser=argument_parser,
            ap_commands=argument_parser.add_argument_group("commands"),
            ap_optional=argument_parser.add_argument_group("optional arguments"),
            ap_required=argument_parser.add_argument_group("required arguments"),
            env_handlers={},
            ini_section_strict={s.name: s.strict for s in config_type.ini_sections_()},
            ini_handlers={},
            cl_flag_handlers={},
            cl_positionals=[],
            validators=[*config_type.validators_()],
        )


@dataclass(frozen=True)
class Processor(Generic[_Config]):
    """
    Configuration processor
    """

    #: Configuration to parse
    config_type: Type[_Config]

    #: Completed argument parser, used only for documentation purposes (CLI and Sphinx)
    argument_parser: argparse.ArgumentParser

    #: Environment variable handlers
    env_handlers: Mapping[str, KVHandler]

    #: INI file processor
    ini_processor: IniProcessor

    #: Command line arguments handler
    cl_handler: CLStdHandler

    #: Dictionary of parameters by field name
    params_by_name: Mapping[str, Param[Any]]

    validators: Sequence[Callable[[_Config], Optional[Err]]]

    @staticmethod
    def process_fields(config_type: Type[_Config]) -> Sequence[Arg]:
        """
        Returns a sequence of the arguments present in a configuration, with updated data

        Args:
            config_type: Configuration to process

        Returns:
            Sequence of arguments
        """
        args: List[Arg] = []
        docs: ClassDoc[_Config] = ClassDoc.make(config_type)
        th = get_type_hints(config_type, include_extras=True)
        for name, typ in th.items():
            arg: Optional[Arg] = None
            if get_origin(typ) is ClassVar:
                a = getattr(config_type, name)
                if isinstance(a, Arg):
                    assert isinstance(a, Expander), "Only commands (Cmd) can be class attributes"
                    arg = a
            if get_origin(typ) is Annotated:
                param = filter_types_single(Param, get_args(typ))
                if param is not None:
                    arg = param
            if arg is not None:
                help_lines = docs[name]
                if help_lines is None:
                    hlp = ""
                else:
                    hlp = "\n".join(help_lines)
                arg = arg.updated(name, hlp, config_type.env_prefix_)
                args.append(arg)
        return args

    @staticmethod
    def make(
        config_type: Type[_Config],
    ) -> Processor[_Config]:
        """
        Creates the processor corresponding to a configuration
        """

        pf = ProcessorFactory.make(config_type)
        for arg in Processor.process_fields(config_type):
            arg.update_processor(pf)

        # if these flags are no longer provided by default, update the overview concept notebook
        # in the documentation
        pf.cl_flag_handlers["-h"] = CLSpecialAction(SpecialAction.HELP)
        pf.cl_flag_handlers["--help"] = CLSpecialAction(SpecialAction.HELP)

        return Processor(
            config_type=config_type,
            argument_parser=pf.argument_parser,
            env_handlers=pf.env_handlers,
            ini_processor=IniProcessor(pf.ini_section_strict, pf.ini_handlers),
            cl_handler=CLStdHandler(pf.cl_flag_handlers, CLPos(pf.cl_positionals)),
            params_by_name=pf.params_by_name,
            validators=pf.validators,
        )

    def _process_config(self, state: State) -> Optional[Err]:
        """
        Processes configuration files if such processing was requested by a handler

        Args:
            state: Mutable state to update

        Returns:
            An optional error
        """
        paths = state.config_files_to_process
        state.config_files_to_process = []
        errors: List[Err] = []
        for p in paths:
            err: Optional[Err] = None
            config_path: Optional[Path] = None
            if p.is_absolute():
                config_path = p
            else:
                if state.root_path is None:
                    err = Err.make(
                        "Relative configuration file path given with no root path known"
                    )
                else:
                    config_path = state.root_path / p
            if config_path is not None:
                err = self.ini_processor.process(config_path, state)
            if err is not None:
                errors.append(err.in_context(ini_file=p))
        return Err.collect(*errors)

    def process_ini_contents(self, ini_contents: str) -> Res[_Config]:
        """
        Processes the configuration in INI format contained in a string

        Args:
            ini_contents: Multiline string containing information in INI format

        Returns:
            The parsed configuration or an error
        """
        state = self._state_with_default_values(None)
        err = self.ini_processor.process_string(ini_contents, state)
        if err is not None:
            return err
        return self._finish_processing_state(state)

    def process_ini_file(self, ini_file_path: Path) -> Res[_Config]:
        """
        Processes the configuration contained in an INI file

        Args:
            ini_file_path: Path to the file to parse

        Returns:
            The parsed configuration or an error
        """
        state = self._state_with_default_values(None)
        err = self.ini_processor.process(ini_file_path, state)
        if err is not None:
            return err
        return self._finish_processing_state(state)

    def process(
        self,
        cwd: Path,
        args: Sequence[str],
        env: Mapping[str, str],
    ) -> Res[Union[_Config, SpecialAction]]:
        """
        Processes command-line arguments (deprecated)

        See also: :meth:`.process_command_line`
        """
        warnings.warn(
            "process has been deprecated, use process_command_line instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.process_command_line(cwd, args, env)

    def _finish_processing_state(self, state: State) -> Res[_Config]:
        """
        Finishes the processing of the state

        This method performs:

        - the collection of parameter values
        - the final validation using validation methods

        Args:
            state: State after parsing all elements, must have :attr:`.State.special_action` set
                   to :data:`None`

        Returns:
            The parsed configuration or an error
        """
        assert state.special_action is None
        errors: List[Err] = []
        collected: Dict[str, Any] = {}
        for name, param in self.params_by_name.items():
            instances = state.instances[name]
            res = param.collector.collect(instances)
            if isinstance(res, Err):
                errors.append(res.in_context(param=name))
            else:
                collected[name] = res

        if errors:
            return Err.collect1(*errors)
        c: _Config = self.config_type(**collected)
        validation_error: Optional[Err] = Err.collect(*[f(c) for f in self.validators])
        if validation_error is not None:
            return validation_error
        else:
            return c

    def _state_with_default_values(self, root_path: Optional[Path]) -> State:
        """
        Returns a new state instance with default values populated

        Args:
            root_path: Optional root path used to resolve configuration file paths
        """
        return State.make(root_path, self.params_by_name.values())

    def process_command_line(
        self,
        cwd: Path,
        args: Sequence[str],
        env: Mapping[str, str],
    ) -> Res[Union[_Config, SpecialAction]]:
        """
        Processes command-line arguments, configuration files and environment variables

        Args:
            cwd: Working directory, used as a base for configuration file relative paths
            args: Command line arguments to parse
            env: Environment variables

        Returns:
            Either a parsed configuration, a special action to execute, or (a list of) errors
        """
        errors: List[Err] = []
        state = self._state_with_default_values(cwd)
        # process environment variables
        for key, value in env.items():
            handler = self.env_handlers.get(key)
            if handler is not None:
                err = handler.handle(value, state)
                if err is not None:
                    errors.append(err.in_context(environment_variable=key))
            err = self._process_config(state)
            if err is not None:
                errors.append(err.in_context(environment_variable=key))
        # process command line arguments
        rest_args: Sequence[str] = args
        while rest_args:
            rest_args, err = self.cl_handler.handle(rest_args, state)
            if err is not None:
                errors.append(err)
            err = self._process_config(state)
            if err is not None:
                errors.append(err)

        if state.special_action is not None:
            return state.special_action

        if errors:
            return Err.collect1(*errors)

        return self._finish_processing_state(state)
