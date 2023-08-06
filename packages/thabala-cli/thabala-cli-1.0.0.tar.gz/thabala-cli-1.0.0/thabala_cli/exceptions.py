"""Exceptions used by Thabala CLI"""


class ThabalaCliException(Exception):
    """
    Base class for all Thabala CLI errors.
    Each custom exception should be derived from this class
    """

    status_code = 500


class ThabalaCliConfigException(ThabalaCliException):
    """Raise when there is configuration problem"""


class ThabalaCliApiException(ThabalaCliException):
    """Raise when there is API response problem"""


class ThabalaCliInfraCodeException(ThabalaCliException):
    """Raise when there is an infra code related problem"""


class ThabalaOperationException(ThabalaCliException):
    """Raise when there is an operation problem"""


class ThabalaNotImplementedException(ThabalaCliException):
    """Raise when functionality is not implemented"""
