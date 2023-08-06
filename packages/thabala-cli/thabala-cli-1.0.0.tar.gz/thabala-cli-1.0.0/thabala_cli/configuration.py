import logging
import os
import pathlib
import shlex
import subprocess
import sys
from collections import OrderedDict
from configparser import _UNSET  # type: ignore
from configparser import ConfigParser
from configparser import NoOptionError
from configparser import NoSectionError
from typing import Dict
from typing import Optional
from typing import Union

from thabala_cli.exceptions import ThabalaCliConfigException
from thabala_cli.utils.module_loading import import_string

log = logging.getLogger(__name__)


def expand_env_var(env_var):
    """
    Expands (potentially nested) env vars by repeatedly applying
    `expandvars` and `expanduser` until interpolation stops having
    any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        env_var = interpolated


def run_command(command):
    """Runs command and returns stdout"""
    with subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    ) as process:
        output, stderr = [
            stream.decode(sys.getdefaultencoding(), "ignore")
            for stream in process.communicate()
        ]
        if process.returncode != 0:
            raise ThabalaCliConfigException(
                f"Cannot execute {command}. Error code is: {process.returncode}. "
                f"Output: {output}, Stderr: {stderr}"
            )

    return output


def _default_config_file_path(file_name: str):
    templates_dir = os.path.join(os.path.dirname(__file__), "config_templates")
    return os.path.join(templates_dir, file_name)


# pylint: disable=too-many-ancestors
class ThabalaCliConfigParser(ConfigParser):
    """Custom Thabala CLI Configparser supporting defaults and deprecated options"""

    # These configuration elements can be fetched as the stdout of commands
    # following the "{section}__{name}__cmd" pattern, the idea behind this
    # is to not store password on boxes in text files.
    sensitive_config_values = set()  # type: ignore

    # This method transforms option names on every read, get, or set operation.
    # This changes from the default behaviour of ConfigParser from lowercasing
    # to instead be case-preserving
    def optionxform(self, optionstr: str) -> str:
        return optionstr

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, default_config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.thabala_cli_defaults = ConfigParser(*args, **kwargs)
        if default_config is not None:
            self.thabala_cli_defaults.read_string(default_config)

        self.is_validated = False

    def validate(self):
        self._validate_config_dependencies()
        self.is_validated = True

    def _validate_config_dependencies(self):
        """
        Validate that config values aren't invalid given other config values
        or system-level limitations and requirements.
        """
        # pylint: disable=unnecessary-pass
        pass

    @staticmethod
    def _env_var_name(section, key):
        return f"THABALA__{section.upper()}__{key.upper()}"

    def _get_env_var_option(self, section, key):
        # must have format THABALA__{SECTION}__{KEY} (note double underscore)
        env_var = self._env_var_name(section, key)
        if env_var in os.environ:
            return expand_env_var(os.environ[env_var])
        # alternatively THABALA__{SECTION}__{KEY}_CMD (for a command)
        env_var_cmd = env_var + "_CMD"
        if env_var_cmd in os.environ:
            # if this is a valid command key...
            if (section, key) in self.sensitive_config_values:
                return run_command(os.environ[env_var_cmd])
        return None

    def _get_cmd_option(self, section, key):
        fallback_key = key + "_cmd"
        # if this is a valid command key...
        if (section, key) in self.sensitive_config_values:
            if super().has_option(section, fallback_key):
                command = super().get(section, fallback_key)
                return run_command(command)
        return None

    def get(self, section, key, **kwargs):
        section = str(section).lower()
        key = str(key).lower()

        option = self._get_environment_variables(key, section)
        if option is not None:
            return option

        option = self._get_option_from_config_file(key, kwargs, section)
        if option is not None:
            return option

        option = self._get_option_from_commands(key, section)
        if option is not None:
            return option

        return self._get_option_from_default_config(section, key, **kwargs)

    def _get_option_from_default_config(self, section, key, **kwargs):
        # ...then the default config
        if self.thabala_cli_defaults.has_option(section, key) or "fallback" in kwargs:
            return expand_env_var(self.thabala_cli_defaults.get(section, key, **kwargs))

        log.warning("section/key [%s/%s] not found in config", section, key)

        raise ThabalaCliConfigException(
            f"section/key [{section}/{key}] not found in config"
        )

    def _get_option_from_commands(self, key, section):
        # ...then commands
        option = self._get_cmd_option(section, key)
        if option:
            return option
        return None

    def _get_option_from_config_file(self, key, kwargs, section):
        # ...then the config file
        if super().has_option(section, key):
            # Use the parent's methods to get the actual config here to be able to
            # separate the config from default config.
            return expand_env_var(super().get(section, key, **kwargs))
        return None

    def _get_environment_variables(self, key, section):
        # first check environment variables
        option = self._get_env_var_option(section, key)
        if option is not None:
            return option
        return None

    def getboolean(self, section, key, **kwargs):
        val = str(self.get(section, key, **kwargs)).lower().strip()
        if "#" in val:
            val = val.split("#")[0].strip()
        if val in ("t", "true", "1"):
            return True
        if val in ("f", "false", "0"):
            return False
        raise ThabalaCliConfigException(
            f'Failed to convert value to bool. Please check "{key}" key in "{section}" section. '
            f'Current value: "{val}".'
        )

    # pylint: disable=no-self-use
    def getint(self, section, key, **kwargs):
        val = self.get(section, key, **kwargs)

        try:
            return int(val)
        except ValueError as value_err:
            raise ThabalaCliConfigException(
                f'Failed to convert value to int. Please check "{key}" key in "{section}" section. '
                f'Current value: "{val}".'
            ) from value_err

    def getfloat(self, section, key, **kwargs):
        val = self.get(section, key, **kwargs)

        try:
            return float(val)
        except ValueError as value_err:
            raise ThabalaCliConfigException(
                f'Failed to convert value to float. Please check "{key}" key in "{section}" section. '
                f'Current value: "{val}".'
            ) from value_err

    def getimport(self, section, key, **kwargs):  # noqa
        """
        Reads options, imports the full qualified name, and returns the object.
        In case of failure, it throws an exception a clear message with the key aad the section names
        :return: The object or None, if the option is empty
        """
        full_qualified_path = conf.get(section=section, key=key, **kwargs)
        if not full_qualified_path:
            return None

        try:
            return import_string(full_qualified_path)
        except ImportError as import_err:
            log.error(import_err)
            raise ThabalaCliConfigException(
                f'The object could not be loaded. Please check "{key}" key in "{section}" section. '
                f'Current value: "{full_qualified_path}".'
            ) from import_err

    def read(self, filenames, encoding=None):
        super().read(filenames=filenames, encoding=encoding)

    def read_dict(self, dictionary, source="<dict>"):
        super().read_dict(dictionary=dictionary, source=source)

    def has_option(self, section, option):
        try:
            # Using self.get() to avoid reimplementing the priority order
            # of config variables (env, config, cmd, defaults)
            # UNSET to avoid logging a warning about missing values
            self.get(section, option, fallback=_UNSET)
            return True
        except (NoOptionError, NoSectionError):
            return False

    def remove_option(self, section, option, remove_default=True):
        """
        Remove an option if it exists in config from a file or
        default config. If both of config have the same option, this removes
        the option in both configs unless remove_default=False.
        """
        if super().has_option(section, option):
            super().remove_option(section, option)

        if self.thabala_cli_defaults.has_option(section, option) and remove_default:
            self.thabala_cli_defaults.remove_option(section, option)

    def getsection(
        self, section: str
    ) -> Optional[Dict[str, Union[str, int, float, bool]]]:
        """
        Returns the section as a dict. Values are converted to int, float, bool
        as required.
        :param section: section from the config
        :rtype: dict
        """
        if not self.has_section(section) and not self.thabala_cli_defaults.has_section(
            section
        ):
            return None

        if self.thabala_cli_defaults.has_section(section):
            _section = OrderedDict(self.thabala_cli_defaults.items(section))
        else:
            _section = OrderedDict()

        if self.has_section(section):
            _section.update(OrderedDict(self.items(section)))

        section_prefix = f"THABALA__{section.upper()}__"
        for env_var in sorted(os.environ.keys()):
            if env_var.startswith(section_prefix):
                key = env_var.replace(section_prefix, "")
                if key.endswith("_CMD"):
                    key = key[:-4]
                key = key.lower()
                _section[key] = self._get_env_var_option(section, key)

        for key, val in _section.items():
            try:
                val = int(val)
            except ValueError:
                try:
                    val = float(val)
                except ValueError:
                    if val.lower() in ("t", "true"):
                        val = True
                    elif val.lower() in ("f", "false"):
                        val = False
            _section[key] = val
        return _section

    def as_dict(
        self,
        display_source=False,
        display_sensitive=False,
        raw=False,
        include_env=True,
        include_cmds=True,
    ) -> Dict[str, Dict[str, str]]:
        """
        Returns the current configuration as an OrderedDict of OrderedDicts.
        :param display_source: If False, the option value is returned. If True,
            a tuple of (option_value, source) is returned. Source is either
            'cli.cfg', 'default', 'env var', or 'cmd'.
        :type display_source: bool
        :param display_sensitive: If True, the values of options set by env
            vars and bash commands will be displayed. If False, those options
            are shown as '< hidden >'
        :type display_sensitive: bool
        :param raw: Should the values be output as interpolated values, or the
            "raw" form that can be fed back in to ConfigParser
        :type raw: bool
        :param include_env: Should the value of configuration from AIRFLOW__
            environment variables be included or not
        :type include_env: bool
        :param include_cmds: Should the result of calling any *_cmd config be
            set (True, default), or should the _cmd options be left as the
            command to run (False)
        :type include_cmds: bool
        :param include_secret: Should the result of calling any *_secret config be
            set (True, default), or should the _secret options be left as the
            path to get the secret from (False)
        :return: Dictionary, where the key is the name of the section and the content is
            the dictionary with the name of the parameter and its value.
        """
        config_sources: Dict[str, Dict[str, str]] = {}
        configs = [
            ("default", self.thabala_cli_defaults),
            ("cli.cfg", self),
        ]

        self._replace_config_with_display_sources(
            config_sources, configs, display_source, raw
        )

        # add env vars and overwrite because they have priority
        if include_env:
            self._include_envs(config_sources, display_sensitive, display_source, raw)

        # add bash commands
        if include_cmds:
            self._include_commands(
                config_sources, display_sensitive, display_source, raw
            )
        return config_sources

    def _include_commands(self, config_sources, display_sensitive, display_source, raw):
        for (section, key) in self.sensitive_config_values:
            opt = self._get_cmd_option(section, key)
            if not opt:
                continue
            if not display_sensitive:
                opt = "< hidden >"
            if display_source:
                opt = (opt, "cmd")
            elif raw:
                opt = opt.replace("%", "%%")
            config_sources.setdefault(section, OrderedDict()).update({key: opt})
            del config_sources[section][key + "_cmd"]

    def _include_envs(self, config_sources, display_sensitive, display_source, raw):
        for env_var in [
            os_environment
            for os_environment in os.environ
            if os_environment.startswith("THABALA__")
        ]:
            try:
                _, section, key = env_var.split("__", 2)
                opt = self._get_env_var_option(section, key)
            except ValueError:
                continue
            if not display_sensitive and env_var != "THABALA__CORE__UNIT_TEST_MODE":
                opt = "< hidden >"
            elif raw:
                opt = opt.replace("%", "%%")
            if display_source:
                opt = (opt, "env var")

            section = section.lower()
            # if we lower key for kubernetes_environment_variables section,
            # then we won't be able to set any Airflow environment
            # variables. Thabala only parse environment variables starts
            # with THABALA__. Therefore, we need to make it a special case.
            if section != "kubernetes_environment_variables":
                key = key.lower()
            config_sources.setdefault(section, OrderedDict()).update({key: opt})

    @staticmethod
    def _replace_config_with_display_sources(
        config_sources, configs, display_source, raw
    ):
        for (source_name, config) in configs:
            for section in config.sections():
                ThabalaCliConfigParser._replace_section_config_with_display_sources(
                    config, config_sources, display_source, raw, section, source_name
                )

    @staticmethod
    def _replace_section_config_with_display_sources(
        config, config_sources, display_source, raw, section, source_name
    ):
        sect = config_sources.setdefault(section, OrderedDict())
        for (k, val) in config.items(section=section, raw=raw):
            if display_source:
                val = (val, source_name)
            sect[k] = val

    def load_test_config(self):
        """
        Load the unit test configuration.
        Note: this is not reversible.
        """
        # remove all sections, falling back to defaults
        for section in self.sections():
            self.remove_section(section)

        # then read test config

        path = _default_config_file_path("default_cli_test.cfg")
        log.info("Reading default test configuration from %s", path)
        self.read_string(_parameterized_config_from_template("default_cli_test.cfg"))
        # then read any "custom" test settings
        log.info("Reading test configuration from %s", TEST_CONFIG_FILE)
        self.read(TEST_CONFIG_FILE)


def get_thabala_home():
    """Get path to Thabala Home"""
    return expand_env_var(os.environ.get("THABALA_HOME", "~/.config/thabala"))


def get_thabala_cli_config(thabala_home):
    """Get Path to cli.cfg path"""
    if "THABALA_CONFIG" not in os.environ:
        return os.path.join(thabala_home, "cli.cfg")
    return expand_env_var(os.environ["THABALA_CONFIG"])


def _parameterized_config_from_template(filename) -> str:
    TEMPLATE_START = (
        "# ----------------------- TEMPLATE BEGINS HERE -----------------------\n"
    )

    path = _default_config_file_path(filename)
    with open(path) as fh:
        for line in fh:
            if line != TEMPLATE_START:
                continue
            return parameterized_config(fh.read().strip())
    raise RuntimeError(f"Template marker not found in {path!r}")


def parameterized_config(template):
    """
    Generates a configuration from the provided template + variables defined in
    current scope
    :param template: a config content templated with {{variables}}
    """
    all_vars = {k: v for d in [globals(), locals()] for k, v in d.items()}
    return template.format(**all_vars)  # noqa


def get_thabala_cli_test_config(thabala_home):
    """Get path to cli_test.cfg"""
    if "THABALA_CLI_TEST_CONFIG" not in os.environ:
        return os.path.join(thabala_home, "cli_test.cfg")
    return expand_env_var(os.environ["THABALA_CLI_TEST_CONFIG"])


def initialize_config():
    """
    Load the config files
    Called for you automatically as part of the boot process.
    """
    global THABALA_HOME

    default_config = _parameterized_config_from_template("default_thabala_cli.cfg")

    conf = ThabalaCliConfigParser(default_config=default_config)

    if conf.getboolean("core", "unit_test_mode"):
        # Load test config only
        if not os.path.isfile(TEST_CONFIG_FILE):
            log.info("Creating new config file for unit tests in: %s", TEST_CONFIG_FILE)
            pathlib.Path(THABALA_HOME).mkdir(parents=True, exist_ok=True)

            with open(TEST_CONFIG_FILE, "w") as file:
                cfg = _parameterized_config_from_template("default_cli_test.cfg")
                file.write(cfg)

        conf.load_test_config()
    else:
        # Load normal config
        if not os.path.isfile(THABALA_CLI_CONFIG):
            log.info("Creating new config file in: %s", THABALA_CLI_CONFIG)
            pathlib.Path(THABALA_HOME).mkdir(parents=True, exist_ok=True)

            with open(THABALA_CLI_CONFIG, "w") as file:
                file.write(default_config)

        log.info("Reading the config from %s", THABALA_CLI_CONFIG)

        conf.read(THABALA_CLI_CONFIG)

        # They _might_ have set unit_test_mode in the cli.cfg, we still
        # want to respect that and then load the unittests.cfg
        if conf.getboolean("core", "unit_test_mode"):
            conf.load_test_config()

    return conf


# Setting THABALA_HOME and THABALA_CLI_CONFIG from environment variables, using
# "~/thabala" and "THABALA_HOME/cli.cfg" respectively as defaults

THABALA_HOME = get_thabala_home()
THABALA_CLI_CONFIG = get_thabala_cli_config(THABALA_HOME)

TEST_CONFIG_FILE = get_thabala_cli_test_config(THABALA_HOME)

conf = initialize_config()
conf.validate()
