import logging
from logging.config import dictConfig

from thabala_cli.configuration import conf
from thabala_cli.exceptions import ThabalaCliConfigException
from thabala_cli.utils.module_loading import import_string

log = logging.getLogger(__name__)


def configure_logging():
    """Configure & Validate Thabala logging"""
    logging_class_path = ""
    try:
        logging_class_path = conf.get("logging", "logging_config_class")
    except ThabalaCliConfigException:
        log.debug("Could not find key logging_config_class in config")

    if logging_class_path:
        try:
            logging_config = import_string(logging_class_path)

            # Make sure that the variable is in scope
            if not isinstance(logging_config, dict):
                raise ValueError("Logging Config should be of dict type")

            log.info(
                "Successfully imported user-defined logging config from %s",
                logging_class_path,
            )
        except Exception as err:
            # Import default logging configurations.
            raise ImportError(
                f"Unable to load custom logging from {logging_class_path} due to {err}"
            ) from err
    else:
        logging_class_path = "thabala_cli.config_templates.thabala_cli_logging_settings.DEFAULT_LOGGING_CONFIG"
        logging_config = import_string(logging_class_path)
        log.debug("Unable to load custom logging, using default config instead")

    try:
        # Try to init logging
        dictConfig(logging_config)
    except ValueError as value_err:
        log.error("Unable to load the config, contains a configuration error.")
        # When there is an error in the config, escalate the exception
        # otherwise Thabala would silently fall back on the default config
        raise value_err

    return logging_class_path
