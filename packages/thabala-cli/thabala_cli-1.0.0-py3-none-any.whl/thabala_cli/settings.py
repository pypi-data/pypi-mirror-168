import logging
import os
from typing import Optional

import pendulum

from thabala_cli.configuration import conf
from thabala_cli.logging_config import configure_logging

log = logging.getLogger(__name__)


TIMEZONE = pendulum.tz.timezone("UTC")
try:
    # pylint: disable=invalid-name
    tz = conf.getboolean("core", "default_timezone")
    if tz == "system":
        TIMEZONE = pendulum.tz.local_timezone()
    else:
        TIMEZONE = pendulum.tz.timezone(tz)
except Exception:  # pylint: disable=broad-except
    pass
log.info("Configured default timezone %s", TIMEZONE)

LOGGING_LEVEL = logging.INFO
LOG_FORMAT = conf.get("logging", "log_format")
SIMPLE_LOG_FORMAT = conf.get("logging", "simple_log_format")
LOGGING_CLASS_PATH: Optional[str] = None

USERNAME: Optional[str] = None
PASSWORD: Optional[str] = None


# pylint: disable=global-statement
def configure_vars():
    """Configure Global Variables from cli.cfg"""
    global USERNAME
    global PASSWORD
    USERNAME = conf.get("default", "USERNAME")
    PASSWORD = conf.get("default", "PASSWORD")


def initialize():
    """Initialize Thabala with all the settings from this file"""
    configure_vars()
    global LOGGING_CLASS_PATH
    LOGGING_CLASS_PATH = configure_logging()
