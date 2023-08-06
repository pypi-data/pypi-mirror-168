import logging

import requests

from thabala_cli.commands.utils.auth_base import AuthBase
from thabala_cli.utils.helpers import raise_thabala_cli_api_exc

log = logging.getLogger(__name__)


class AuthByPassword(AuthBase):
    """Authenticate by user and password via the default Thabala backend database"""

    def __init__(self, api_base_url, username, password):
        super().__init__(api_base_url)

        self._username = username
        self._password = password

    def authenticate(self):
        """User and password based authentication"""
        log.debug("Authenticating by password authenticator")

        try:
            response = requests.post(
                f"{self._api_base_url}/auth/token",
                headers=self._headers,
                json={
                    "grant_type": "password",
                    "username": self._username,
                    "password": self._password,
                },
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise_thabala_cli_api_exc(err, response.json())
        except Exception as err:
            raise_thabala_cli_api_exc(err)

        access_token = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]

        return access_token, refresh_token
