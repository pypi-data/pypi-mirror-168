from __future__ import annotations

import os


def get_module_of_directory(directory: str) -> str:

    parent_dir = os.path.dirname(directory)
    base = os.path.basename(directory)
    if '__init__.py' in os.listdir(parent_dir):
        result = get_module_of_directory(parent_dir) + '.' + base
        return result
    else:
        return base


def get_module_of_working_directory() -> str:
    return get_module_of_directory(os.path.abspath(os.getcwd()))
