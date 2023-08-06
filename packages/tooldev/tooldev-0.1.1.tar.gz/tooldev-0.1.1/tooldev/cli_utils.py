from __future__ import annotations

import typing

import toolcli
import tooldev


def get_cli_styles() -> toolcli.StyleTheme:
    return {
        'title': 'bold #ce93f9',
        'metavar': '#8be9fd',
        'description': '#b9f29f',
        'content': '#f1fa8c',
        'option': '#64aaaa',
        'comment': '#6272a4',
    }


def run_cli(
    raw_command: str | None = None,
    **toolcli_kwargs: typing.Any,
) -> None:

    command_index: typing.Mapping[tuple[str, ...], str] = {
        (): 'tooldev.commands.root_command',
        ('lsp',): 'tooldev.commands.lsp_command',
        ('pwp',): 'tooldev.commands.pwp_command',
        ('shell',): 'tooldev.commands.shell_command',
    }

    styles = get_cli_styles()

    config: toolcli.CLIConfig = {
        'base_command': 'td',
        'description': 'td is a suite of CLI tools for python development',
        'version': tooldev.__version__,
        'style_theme': styles,
        'include_standard_subcommands': True,
        'include_debug_arg': True,
    }

    toolcli_kwargs = dict({'config': config}, **toolcli_kwargs)

    toolcli.run_cli(
        raw_command=raw_command,
        command_index=command_index,
        **toolcli_kwargs,
    )

