"""

These need to be added to a shell config directly
- e.g. running `cd` in a subprocess does not actually change the working dir
"""
from __future__ import annotations

import toolcli


help_message = """print tooldev settings that should be added to shell config

add this content to your shell config
e.g. `td shell 1>> ~.profile`"""


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': shell_command,
        'help': help_message,
    }


tooldev_shell_config = """
alias lsp="td lsp"
alias pwp="td pwp"

function gcd () { cd $(git rev-parse --show-toplevel); }
function cdg () { cd $(git rev-parse --show-toplevel); }
function pcd () { cd $(realpath $(python3 -c "import $1; print($1.__path__[0])")); }
function cdp () { cd $(realpath $(python3 -c "import $1; print($1.__path__[0])")); }

function importtime() {
    python3 -X importtime -c "import $1" 2>/tmp/tuna.log;
    tuna /tmp/tuna.log;
}

function pdep () {
    echo "Dependency tree"
    echo ""
    pipdeptree -w silence -p $1
    echo ""
    echo ""
    echo "Unique dependencies"
    pipdeptree -w silence -p $1 | awk -v col=2 '{print tolower($col)}' | sort | uniq
    echo ""
    echo "Total unique dependencies:" $(pipdeptree -w silence -p $1 | awk -v col=2 '{print tolower($col)}' | sort | uniq | wc -l)
}
"""


def shell_command() -> None:
    print(tooldev_shell_config)
