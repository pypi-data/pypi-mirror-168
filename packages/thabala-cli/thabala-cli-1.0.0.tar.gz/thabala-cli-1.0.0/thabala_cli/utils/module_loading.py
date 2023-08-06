from importlib import import_module


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribution/class designated by the
    last name in the path.. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as value_err:
        raise ImportError(
            f"{dotted_path} doesn't look like a module path"
        ) from value_err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as attr_err:
        raise ImportError(
            f'Module "{module_path}" does not define a "{class_name}" attribute/class'
        ) from attr_err
