"""
Example code of ``calculator6.py`` integrated into configpile as workaround
"""
import argparse
from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import Sequence

from typing_extensions import Annotated

from configpile import Config, Param, Positional, parsers


@dataclass(frozen=True)
class Calc(Config):
    """
    Command-line tool that sums an arbitrary number of floating point values
    """

    prog_ = "calculator6.py"

    config: Annotated[Sequence[Path], Param.config(help="INI configuration files to parse")]

    values: Annotated[
        Sequence[float],
        Param.append1(
            parsers.float_parser,
            positional=Positional.ZERO_OR_MORE,
            short_flag_name=None,
            long_flag_name=None,
            help="Values to sum",
        ),
    ]

    operation: Annotated[
        str,
        Param.store(
            parsers.Parser.from_choices(["+", "*"]),
            default_value="+",
            help='Operation to perform, either addition "+" or multiplication "*"',
        ),
    ]

    digits: Annotated[
        int,
        Param.store(
            parsers.int_parser.validated(lambda i: i > 0, "Must be a positive integer"),
            default_value="3",
            env_var_name="DIGITS",
            help="""
Number of digits to display

This number of digits can also be set with the environment variable
``DIGITS``
            """,
        ),
    ]


def argument_parser() -> argparse.ArgumentParser:
    """
    Returns a parser for use for sphinx-argparse
    """
    return Calc.get_argument_parser_()


if __name__ == "__main__":
    c = Calc.from_command_line_()
    fmt_string = f"%.{c.digits}f"
    if c.operation == "+":
        print(fmt_string % sum(c.values))
    elif c.operation == "*":
        print(fmt_string % prod(c.values))
