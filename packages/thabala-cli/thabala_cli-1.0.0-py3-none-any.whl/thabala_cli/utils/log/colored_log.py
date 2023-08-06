"""Class responsible for colouring logs based on log level."""
# pylint: disable=unsubscriptable-object

import re
import sys
from logging import LogRecord
from typing import Any
from typing import Union

from colorlog import TTYColoredFormatter
from colorlog.escape_codes import esc
from colorlog.escape_codes import escape_codes

DEFAULT_COLORS = {
    "DEBUG": "green",
    "INFO": "",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red",
}

BOLD_ON = escape_codes["bold"]
BOLD_OFF = esc("22")


class CustomTTYColoredFormatter(TTYColoredFormatter):
    """
    Custom log formatter which extends `colored.TTYColoredFormatter`
    by adding attributes to message arguments and coloring error
    traceback.
    """

    def __init__(self, *args, **kwargs):
        kwargs["stream"] = sys.stdout or kwargs.get("stream")
        kwargs["log_colors"] = DEFAULT_COLORS
        super().__init__(*args, **kwargs)

    @staticmethod
    def _color_arg(arg: Any) -> Union[str, float, int]:
        if isinstance(arg, (int, float)):
            # In case of %d or %f formatting
            return arg
        return BOLD_ON + str(arg) + BOLD_OFF

    @staticmethod
    def _count_number_of_arguments_in_message(record: LogRecord) -> int:
        matches = re.findall(r"%.", record.msg)
        return len(matches) if matches else 0

    def _color_record_args(self, record: LogRecord) -> LogRecord:
        if isinstance(record.args, (tuple, list)):
            record.args = tuple(self._color_arg(arg) for arg in record.args)
        elif isinstance(record.args, dict):
            if self._count_number_of_arguments_in_message(record) > 1:
                # Case of logging.debug("a %(a)d b %(b)s", {'a':1, 'b':2})
                record.args = {
                    key: self._color_arg(value) for key, value in record.args.items()
                }
            else:
                # Case of single dict passed to formatted string
                record.args = self._color_arg(record.args)  # type: ignore
        elif isinstance(record.args, str):
            record.args = self._color_arg(record.args)
        return record

    def _color_record_traceback(self, record: LogRecord) -> LogRecord:
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

            if record.exc_text:
                record.exc_text = (
                    self.color(self.log_colors, record.levelname)
                    + record.exc_text
                    + escape_codes["reset"]
                )

        return record

    def format(self, record: LogRecord) -> str:
        try:
            if self.stream.isatty():
                record = self._color_record_args(record)
                record = self._color_record_traceback(record)
            return super().format(record)
        except ValueError:  # I/O operation on closed file
            from logging import Formatter

            return Formatter().format(record)
