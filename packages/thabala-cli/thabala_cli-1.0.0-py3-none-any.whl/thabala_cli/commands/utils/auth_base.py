import urllib

from thabala_cli.exceptions import ThabalaNotImplementedException


class AuthBase:
    """Authenticator interface."""

    def __init__(self, api_base_url) -> None:
        self._api_base_url = api_base_url
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def authenticate(self):
        raise ThabalaNotImplementedException
