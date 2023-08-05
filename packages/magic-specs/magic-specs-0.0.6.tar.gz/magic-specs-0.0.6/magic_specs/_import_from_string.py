from importlib import import_module
from sys import modules
from typing import Any


__all__ = [
    "import_from_string",
]


def import_from_string(string: str) -> Any:
    """Attempt to import from a dot import string representation.

    :param string: String to attempt to import with.
    :raises ImportError: Could not import from string.
    """

    msg = f"Could not import {string!r}"
    try:
        module_path, class_name = string.rsplit(".", 1)
    except ValueError as error:
        raise ImportError(f"{msg}: Not a valid module path.") from error

    if module_path not in modules or (
        # Module is not fully initialized.
        getattr(modules[module_path], "__spec__", None) is not None
        and getattr(modules[module_path].__spec__, "_initializing", False) is True
    ):
        try:
            import_module(module_path)
        except ImportError as error:
            raise ImportError(f"{msg}: {error}.") from error

    try:
        return getattr(modules[module_path], class_name)
    except AttributeError as error:
        raise ImportError(f"{msg}: Module {module_path!r} does not define {class_name!r}.") from error
