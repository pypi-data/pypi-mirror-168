from __future__ import annotations

import toolcli

from .. import directory_utils


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': pwp_command,
        'help': 'print package or module corresponding to working directory',
    }


def pwp_command() -> None:
    module = directory_utils.get_module_of_working_directory()
    print(module)
