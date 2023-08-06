from __future__ import annotations

import importlib
import typing

import toolcli

from .. import directory_utils
from .. import namespace_utils


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': lsp_command,
        'help': 'list items inside package namespace',
        'args': [
            {
                'name': 'package_or_module',
                'help': 'package or submodule to list',
                'nargs': '?',
            },
            {
                'name': ['--verbose', '-v'],
                'help': 'enable verbose mode',
                'action': 'store_true',
            },
            {
                'name': ('--modules', '-m'),
                'help': 'display modules and hide other sections',
                'action': 'store_true',
            },
            {
                'name': ('--functions', '-f'),
                'help': 'display functions and hide other sections',
                'action': 'store_true',
            },
            {
                'name': ('--classes', '-c'),
                'help': 'display functions and hide other sections',
                'action': 'store_true',
            },
            {
                'name': ('--exceptions', '-e'),
                'help': 'display exceptions and hide other sections',
                'action': 'store_true',
            },
            {
                'name': ('--dunder', '-d'),
                'help': 'display dunder and hide other sections',
                'action': 'store_true',
            },
            {
                'name': ('--other', '-o'),
                'help': 'display other section and hide other sections',
                'action': 'store_true',
            },
        ],
        'examples': [
            '',
            'numpy',
            'numpy.linalg',
            'numpy.linalg -f -c',
        ],
    }


def lsp_command(
    package_or_module: str,
    verbose: bool,
    modules: bool,
    functions: bool,
    classes: bool,
    exceptions: bool,
    dunder: bool,
    other: bool,
) -> None:

    if package_or_module is None:
        package_name = directory_utils.get_module_of_working_directory()
    else:
        package_name = package_or_module

    package = importlib.import_module(package_name)

    if modules or functions or classes or dunder or other:
        raw_sections: typing.Sequence[tuple[str, bool]] = [
            ('title', True),
            ('internal_modules', modules),
            ('external_modules', modules),
            ('functions', functions),
            ('classes', classes),
            ('exceptions', exceptions),
            ('dunder', dunder),
            ('other', other),
        ]
        sections = [name for name, value in raw_sections if value]
    else:
        sections = None
    namespace_utils.print_module_summary(
        package,
        sections=sections,
        verbose=verbose,
    )
