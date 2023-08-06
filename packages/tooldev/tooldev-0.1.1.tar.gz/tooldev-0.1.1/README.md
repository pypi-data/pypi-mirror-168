
# tooldev

toolbox for terminal-based python development


## Installation

1. Install python package `pip install tooldev`
2. Add entries to shell config `tooldev shell 1>.profile`


## CLI Commands

- `cdp <package>[.<submodule>]`: change directory that of package or module
- `pcd <package>[.<submodule>]`: change directory that of package or module
- `cdg`: change directory to root of git repository
- `gcd`: change directory to root of git repository
- `pdep <package>`: print nested dependencies of a package
- `pwp`: print python package corresponding to current working directory
- `lsp [<package>[.<submodule>]]`: list contents of package or module or working directory
- `importtime <package>[.<submodule>]`: open flame graph of import times for package or module


## Other recommended libraries
- [tuna](https://github.com/nschloe/tuna)
