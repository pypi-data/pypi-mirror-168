"""Thabala logging settings"""
from typing import Any
from typing import Dict

from thabala_cli.configuration import conf
from thabala_cli.exceptions import ThabalaCliException

# TODO: Logging format and level should be configured
# in this file instead of from thabala.cfg. Currently
# there are other log format and level configurations in
# settings.py and cli.py.
LOG_LEVEL: str = conf.get("logging", "LOGGING_LEVEL").upper()

LOG_FORMAT: str = conf.get("logging", "LOG_FORMAT")

COLORED_LOG_FORMAT: str = conf.get("logging", "COLORED_LOG_FORMAT")

COLORED_LOG: bool = conf.getboolean("logging", "COLORED_CONSOLE_LOG")

COLORED_FORMATTER_CLASS: str = conf.get("logging", "COLORED_FORMATTER_CLASS")

BASE_LOG_FOLDER: str = conf.get("logging", "BASE_LOG_FOLDER")

DEFAULT_LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "thabala_cli": {"format": LOG_FORMAT},
        "thabala_cli_colored": {
            "format": COLORED_LOG_FORMAT if COLORED_LOG else LOG_FORMAT,
            "class": COLORED_FORMATTER_CLASS if COLORED_LOG else "logging.Formatter",
        },
    },
    "handlers": {
        "console": {
            "class": "thabala_cli.utils.log.logging_mixin.RedirectStdHandler",
            "formatter": "thabala_cli_colored",
            "stream": "sys.stdout",
        },
    },
    "loggers": {},
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}
