from __future__ import annotations

import toolcli


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': root_command,
        'help': 'insert',
        'args': [
            {
                'name': 'query',
                'nargs': '*',
                'help': 'address, block number, tx hash, or ERC20 symbol',
            }
        ],
        'extra_data': ['parse_spec'],
    }


def root_command(query: str, parse_spec: toolcli.ParseSpec) -> None:

    if len(query) == 0:
        toolcli.command_utils.execution.execute_other_command_sequence(
            command_sequence=('help',),
            args={'parse_spec': parse_spec},
            parse_spec=parse_spec,
        )
    else:
        raise Exception('unknown query: ' + str(query))
