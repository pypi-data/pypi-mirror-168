import pathlib

from . import exceptions


class register:
    """
    A class that acts as a global singelton. Get a dict of hooks by
    calling `register.hooks`
    """

    hooks = {}
    callables = {}
    "List of registered hooks"

    @classmethod
    def hook_entrypoint(cls, section: str, option: str, entrypoint: str):
        if entrypoint:
            if not isinstance(entrypoint, str) or not entrypoint.startswith(
                "builtins:"
            ):
                raise exceptions.CommandFail(
                    f"Hook configuration error: {entrypoint}: Only builtin hooks is supported for now."
                )
            if entrypoint not in cls.callables:
                raise exceptions.CommandFail(
                    f"Hook configuration error: {entrypoint} not found"
                )
            if section not in cls.hooks:
                cls.hooks[section] = {}
            cls.hooks[section][option] = cls.callables[entrypoint]

    @classmethod
    def hook_callable(cls, name: str):
        """
        A simple decorator to register hook `callable`.
        Get a dict of hook callables by calling `register.callables`.

        .. code-block:: py

            @register.hook_function("function:print_debugger")
            def print_debugger_func(*args, **kwargs):
                print(args, kwargs)
                return args, kwargs
        """

        def wrap(c):
            cls.callables[name] = c
            return c

        return wrap


@register.hook_callable("builtins:basedir:add-as-prefix")
def builtins_basedir(root, *args, **kwargs):
    """
    Add cwd base name as a prefix to root name.
    Should only be used with the ``hook:transform-root`` option
    for now:

    .. code-block:: ini

        [install:subprojdir]
        hook:transform-root = builtins:basedir:add-as-prefix

    """
    cwd = pathlib.Path.cwd()
    new_root = f"{cwd.stem}_{root}"
    return new_root


def transform_root(install_to: str, root: str, locals: dict):
    opt = "hook:transform-root"
    transform_root = ""

    if install_to in register.hooks:
        if opt in register.hooks[install_to]:
            fn = register.hooks[install_to][opt]
            transform_root = fn(root, locals)
    return transform_root
