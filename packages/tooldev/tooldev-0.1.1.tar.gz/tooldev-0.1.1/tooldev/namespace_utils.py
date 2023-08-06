from __future__ import annotations

import typing

import toolcli
import toolstr

from . import cli_utils

if typing.TYPE_CHECKING:
    import types

    GenericModule = typing.Union[
        types.ModuleType, typing.Mapping[str, typing.Any]
    ]


def get_module_attrs(
    module: GenericModule,
) -> typing.Mapping[str, typing.Mapping[str, typing.Any]]:
    """return list of items in module namespace"""

    # convert to dict
    module = module_to_dict(module)

    module_name = module.get('__name__', '')
    moduletype = type(toolstr)
    functiontype = type(get_module_attrs)

    # sort module attributes into categories
    internal_modules = {}
    external_modules = {}
    functions = {}
    dunder = {}
    exceptions = {}
    classes = {}
    other = {}
    for key in sorted(module.keys()):
        value = module[key]
        if isinstance(value, moduletype):
            value = module_to_dict(value)
            submodule_name = value.get('__name__', key)
            if module_name != '' and submodule_name.startswith(module_name):
                internal_modules[submodule_name] = value
            else:
                external_modules[submodule_name] = value
        elif isinstance(value, functiontype):
            functions[value.__name__] = value
        elif key.startswith('__') and key.endswith('__'):
            dunder[key] = value
        elif isinstance(value, type) and issubclass(value, BaseException):
            exceptions[key] = value
        elif isinstance(value, type):
            classes[key] = value
        else:
            other[key] = value

    return {
        'internal_modules': internal_modules,
        'external_modules': external_modules,
        'functions': functions,
        'dunder': dunder,
        'exceptions': exceptions,
        'classes': classes,
        'other': other,
    }


def get_combined_modules(
    modules: typing.Sequence[GenericModule],
) -> GenericModule:

    modules = [module_to_dict(module) for module in modules]

    all_keys = [key for module in modules for key in module.keys()]
    unique_keys = {key for key in all_keys if all_keys.count(key) == 1}

    unique_module = {
        key: value
        for module in modules
        for key, value in module.items()
        if key in unique_keys
    }

    conflict_modules = [
        {key: value for key, value in module.items() if key not in unique_keys}
        for module in modules
    ]

    return {
        'unique': unique_module,
        'nonunique': conflict_modules,
    }


def module_to_dict(module: GenericModule) -> typing.Mapping[str, typing.Any]:
    moduletype = type(toolstr)

    if isinstance(module, dict):
        return module
    elif isinstance(module, moduletype):
        return vars(module)
    else:
        raise Exception('unknown module format: ' + str(module))


def print_module_summary(
    module: GenericModule,
    *,
    max_width: int | None = None,
    sections: typing.Sequence[str] | None = None,
    verbose: bool = False,
) -> None:

    if max_width is None:
        max_width = toolcli.get_n_terminal_cols()

    if sections is None:
        sections = [
            'title',
            'internal_modules',
            'external_modules',
            'functions',
            'classes',
            'exceptions',
            'dunder',
            'other',
        ]

    module = module_to_dict(module)
    module_attrs = get_module_attrs(module)

    styles = cli_utils.get_cli_styles()

    if 'title' in sections:
        toolstr.print_text_box(
            'Namespace Summary for ' + module.get('__name__', '\[unnamed]'),
            style=styles['title'],
        )
        print()
        toolstr.print_bullet(
            key='items in module namespace:',
            value=len(module),
            bullet_str='',
            styles=styles,
        )
        for key, value in module_attrs.items():
            toolstr.print_bullet(key=key, value=len(value), styles=styles)

    # internal modules
    if 'internal_modules' in sections:
        print()
        toolstr.print_text_box('Internal Modules', style=styles['title'])
        rows = [
            [
                module.get('__name__', ''),
                _process_docstring(module.get('__doc__')),
            ]
            for module_name, module in sorted(
                module_attrs['internal_modules'].items()
            )
        ]
        rows = sorted(rows)
        toolstr.print_table(
            rows,
            compact=2,
            labels=['module', 'description'],
            add_row_index=True,
            column_justify={'module': 'left', 'description': 'left'},
            label_justify='left',
            border=styles['comment'],
            label_style=styles['title'],
            column_styles={
                'module': styles['option'],
                '': styles['comment'],
            },
            max_table_width=max_width,
        )

    # external modules
    if 'external_modules' in sections:
        print()
        toolstr.print_text_box('External Modules', style=styles['title'])
        rows = [
            [
                module.get('__name__', ''),
                _process_docstring(module.get('__doc__')),
            ]
            for module_name, module in sorted(
                module_attrs['external_modules'].items()
            )
        ]
        toolstr.print_table(
            rows,
            compact=1,
            labels=['module', 'description'],
            add_row_index=True,
            column_justify={'module': 'left', 'description': 'left'},
            label_justify='left',
            border=styles['comment'],
            label_style=styles['title'],
            column_styles={
                'module': styles['option'],
                '': styles['comment'],
            },
            max_table_width=max_width,
        )

    # functions
    if 'functions' in sections:
        print()
        toolstr.print_text_box('Functions', style=styles['title'])

        rows = []
        for function_name, function in module_attrs['functions'].items():

            function_module = function.__module__.split(
                module.get('__name__', ' ')
            )[-1]
            if not verbose and len(function_module) > 25:
                clips = 0
                if function_module.startswith('.'):
                    function_module = function_module[1:]
                    clips += 1
                while len(function_module) > 25:
                    new_function_module = '.'.join(function_module.split('.')[1:])
                    clips += 1
                    function_module = new_function_module
                function_module = '.' * clips + function_module

            docstring = _process_docstring(function.__doc__)
            row = [
                function_module,
                function_name,
                docstring,
            ]
            rows.append(row)

        toolstr.print_table(
            rows,
            compact=2,
            labels=[
                'module',
                'function',
                'description',
            ],
            add_row_index=True,
            label_justify='left',
            column_justify={
                'module': 'left',
                'function': 'left',
                'description': 'left',
            },
            border=styles['comment'],
            label_style=styles['title'],
            column_styles={
                'module': styles['option'],
                'function': styles['description'],
                '': styles['comment'],
            },
            max_table_width=max_width,
        )

    if 'classes' in sections:
        print()
        toolstr.print_text_box('Classes', style=styles['title'])

        rows = []
        for class_name, class_class in module_attrs['classes'].items():
            docstring = _process_docstring(class_class.__doc__)
            row = [
                class_name,
                docstring,
            ]
            rows.append(row)

        toolstr.print_table(
            rows,
            compact=2,
            labels=[
                'class',
                'description',
            ],
            add_row_index=True,
            label_justify='left',
            column_justify={
                'class': 'left',
                'description': 'left',
            },
            border=styles['comment'],
            label_style=styles['title'],
            column_styles={
                'class': styles['description'],
                '': styles['comment'],
            },
            max_table_width=max_width,
        )

    if 'exceptions' in sections:
        print()
        toolstr.print_text_box('Exceptions', style=styles['title'])

        rows = []
        for exception_name, exception in module_attrs['exceptions'].items():
            docstring = _process_docstring(exception.__doc__)
            row = [
                exception_name,
                docstring,
            ]
            rows.append(row)

        toolstr.print_table(
            rows,
            compact=2,
            labels=[
                'exception',
                'description',
            ],
            add_row_index=True,
            label_justify='left',
            column_justify={
                'exception': 'left',
                'description': 'left',
            },
            border=styles['comment'],
            label_style=styles['title'],
            column_styles={
                'exception': styles['description'],
                '': styles['comment'],
            },
            max_table_width=max_width,
        )

    # dunder
    if 'dunder' in sections:
        print()
        toolstr.print_text_box('Dunder', style=styles['title'])
        rows = [
            [key, type(value)] for key, value in module_attrs['dunder'].items()
        ]
        toolstr.print_table(
            rows,
            labels=['name', 'type'],
            add_row_index=True,
            compact=2,
            border=styles['comment'],
            label_style=styles['title'],
            column_styles={
                'name': styles['option'],
                'type': styles['description'],
                '': styles['comment'],
            },
            max_table_width=max_width,
        )

    # other
    if 'other' in sections:
        print()
        toolstr.print_text_box('Other', style=styles['title'])
        rows = [
            [key, type(value)] for key, value in module_attrs['other'].items()
        ]
        toolstr.print_table(
            rows,
            labels=['name', 'type'],
            add_row_index=True,
            compact=2,
            border=styles['comment'],
            label_style=styles['title'],
            column_styles={
                'name': styles['option'],
                'type': styles['description'],
                '': styles['comment'],
            },
            max_table_width=max_width,
        )


def _process_docstring(docstring: str | None) -> str | None:
    if isinstance(docstring, str):
        lines = docstring.split('\n')
        for line in lines:
            if line.strip('=') != '':
                return line.lstrip()
        return ''
    return docstring
