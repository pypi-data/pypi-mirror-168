__all__ = ["version"]

try:
    from importlib import metadata  # type: ignore
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata  # type: ignore

version = metadata.version("thabala-cli")
del metadata
