import json
import logging
import os
import socket
import sys
import time
import urllib
import webbrowser

import requests

from thabala_cli.commands.utils.auth_base import AuthBase
from thabala_cli.exceptions import ThabalaCliApiException
from thabala_cli.exceptions import ThabalaOperationException
from thabala_cli.utils.helpers import raise_thabala_cli_api_exc

log = logging.getLogger(__name__)

BUF_SIZE = 16384


class AuthByWebBrowser(AuthBase):
    """Authenticates user by web browser."""

    def __init__(self, api_base_url, webbrowser_pkg=None, socket_pkg=None):
        super().__init__(api_base_url)

        self._protocol = None
        self._host = None
        self._port = None
        self._code = None
        self._state = None
        self._client_id = None
        self._consent_cache_id_token = True
        self._application = "Thabala CLI"
        self._webbrowser = webbrowser if webbrowser_pkg is None else webbrowser_pkg
        self._socket = socket.socket if socket_pkg is None else socket_pkg
        self._origin = None

    def authenticate(self):
        """Web browser based authentication"""
        log.debug("Authenticating by password authenticator")
        tokens = None

        socket_connection = self._socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(
                "Initiating login request with your identity provider. A "
                "browser window should have opened for you to complete the "
                "login. If you can't see it, check existing browser windows, "
                "or your OS settings. Press CTRL+C to abort and try again...",
                file=sys.stderr,
            )

            log.debug("step 1: query GS to obtain OAuth2 urls")
            authorize_url = self._get_authorize_url(callback_port=None)
            if not authorize_url:
                raise ThabalaOperationException(
                    "Authorized URL not found. Is your Thabala "
                    "instance configured to use external browser "
                    "based authentication?"
                )
            self._process_authorize_url(authorize_url)

            log.debug("step 2: start local server to handle callback url")
            try:
                socket_connection.bind(
                    (
                        os.getenv("THABALA_AUTH_SOCKET_ADDR", self._host),
                        int(os.getenv("THABALA_AUTH_SOCKET_PORT", self._port)),
                    )
                )
            except socket.gaierror as ex:
                if ex.args[0] == socket.EAI_NONAME:
                    raise ThabalaOperationException(
                        "localhost is not found. "
                        "Ensure /etc/hosts has localhost entry."
                    )
                else:
                    raise ex
            except TypeError as ex:
                if not self._host:
                    raise ThabalaCliApiException("Callback host is not defined")
                if not self._port:
                    raise ThabalaOperationException("Callback port is not defined")
                else:
                    raise ex
            socket_connection.listen(0)  # no backlog

            log.debug("step 3: open a browser")
            if not self._webbrowser.open_new(authorize_url):
                print(
                    "We were unable to open a browser window for you, "
                    "please open the following url manually then paste the "
                    "URL you are redirected to into the terminal.",
                    file=sys.stderr,
                )
                print(f"URL: {authorize_url}", file=sys.stderr)
                url = input("Enter the URL the authorize URL redirected you to: ")
                self._process_get_url(url)
                if not self._code or not self._state:
                    # Input contained no token, either URL was incorrectly pasted,
                    # empty or just wrong
                    raise ThabalaCliApiException(
                        "Unable to open a browser in this environment and "
                        "auth response contained no code or state."
                    )

            else:
                log.debug("step 4: accept token")
                self._receive_browser_code(socket_connection)
                tokens = self._get_tokens()

        finally:
            socket_connection.close()

        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        return access_token, refresh_token

    def _receive_browser_code(self, socket_connection):
        """Receives auth token from the web browser."""
        while True:
            socket_client, _ = socket_connection.accept()
            try:
                # Receive the data in small chunks and transmit it
                data = socket_client.recv(BUF_SIZE).decode("utf-8").split("\r\n")

                if not self._process_options(data, socket_client):
                    self._process_receive_browser_code(data, socket_client)
                    break
            finally:
                socket_client.shutdown(socket.SHUT_RDWR)
                socket_client.close()

    def _process_options(self, data, socket_client):
        """Allows JS Ajax access to this endpoint."""
        for line in data:
            if line.startswith("OPTIONS "):
                break
        else:
            return False

        AuthByWebBrowser._get_user_agent(data)
        requested_headers, requested_origin = AuthByWebBrowser._check_post_requested(
            data
        )
        if not requested_headers:
            return False

        if not self._validate_origin(requested_origin):
            # validate Origin and fail if not match with the server.
            return False

        self._origin = requested_origin
        content = [
            "HTTP/1.1 200 OK",
            "Date: {}".format(
                time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
            ),
            "Access-Control-Allow-Methods: POST, GET",
            f"Access-Control-Allow-Headers: {requested_headers}",
            "Access-Control-Max-Age: 86400",
            f"Access-Control-Allow-Origin: {self._origin}",
            "",
            "",
        ]
        socket_client.sendall("\r\n".join(content).encode("utf-8"))
        return True

    def _validate_origin(self, requested_origin):
        ret = urllib.parse.urlsplit(requested_origin)
        netloc = ret.netloc.split(":")
        host_got = netloc[0]
        port_got = (
            netloc[1] if len(netloc) > 1 else (443 if self._protocol == "https" else 80)
        )

        return (
            ret.scheme == self._protocol
            and host_got == self._host
            and port_got == self._port
        )

    def _process_receive_browser_code(self, data, socket_client):
        if not self._process_get(data) and not self._process_post(data):
            return  # error

        content = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/html",
        ]
        if self._origin:
            data = {"consent": self._consent_cache_id_token}
            msg = json.dumps(data)
            content.append(f"Access-Control-Allow-Origin: {self._origin}")
            content.append("Vary: Accept-Encoding, Origin")
        else:
            msg = """
            <!DOCTYPE html><html><head><meta charset="UTF-8"/>
            <title>Thabala Authentication Response</title></head>
            <body>
            Your identity was confirmed and propagated to {}.
            You can close this window now and go back where you started from.
            </body></html>""".format(
                self._application
            )
        content.append(f"Content-Length: {len(msg)}")
        content.append("")
        content.append(msg)

        socket_client.sendall("\r\n".join(content).encode("utf-8"))

    @staticmethod
    def _check_post_requested(data):
        request_line = None
        header_line = None
        origin_line = None
        for line in data:
            if line.startswith("Access-Control-Request-Method:"):
                request_line = line
            elif line.startswith("Access-Control-Request-Headers:"):
                header_line = line
            elif line.startswith("Origin:"):
                origin_line = line

        if (
            not request_line
            or not header_line
            or not origin_line
            or request_line.split(":")[1].strip() != "POST"
        ):
            return None, None

        return (
            header_line.split(":")[1].strip(),
            ":".join(origin_line.split(":")[1:]).strip(),
        )

    def _process_authorize_url(self, url: str) -> None:
        parsed_authorize_url = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        if (
            "redirect_uri" not in parsed_authorize_url
            or "state" not in parsed_authorize_url
        ):
            return

        # Get callback URI properties
        parsed_redirect_uri = urllib.parse.urlparse(
            parsed_authorize_url["redirect_uri"][0]
        )
        if not parsed_redirect_uri.port:
            raise ThabalaOperationException(
                "Redirect URI callback port is not included in "
                f"the authentication URL: {url}"
            )
        self._protocol = parsed_redirect_uri.scheme
        self._host = parsed_redirect_uri.hostname
        self._port = parsed_redirect_uri.port

        # Get state
        self._state = parsed_authorize_url["state"][0]
        self._client_id = parsed_authorize_url["client_id"][0]

    def _process_get_url(self, url: str) -> None:
        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        if "code" not in parsed or "state" not in parsed:
            return
        if not parsed["code"][0] or not parsed["state"][0]:
            return
        self._code = parsed["code"][0]

        if parsed["state"][0] != self._state:
            raise ThabalaCliApiException(
                "The requested authentication state " "doesn't match the received one"
            )

    def _process_get(self, data):
        for line in data:
            if line.startswith("GET "):
                target_line = line
                break
        else:
            return False

        self._get_user_agent(data)
        _, url, _ = target_line.split()
        self._process_get_url(url)
        return True

    def _process_post(self, data):
        for line in data:
            if line.startswith("POST "):
                break
        else:
            raise ThabalaCliApiException(
                "Invalid HTTP request from web browser. "
                "Idp authentication could have failed."
            )

        self._get_user_agent(data)
        try:
            # parse the response as JSON
            payload = json.loads(data[-1])
            parsed_state = payload.get("state")
            self._code = payload.get("code")
            self._consent_cache_id_token = payload.get("consent", True)
        except Exception:
            # key=value form.
            parsed_state = urllib.parse.parse_qs(data[-1])["state"][0]
            self._code = urllib.parse.parse_qs(data[-1])["code"][0]

        if parsed_state != self.state:
            raise ThabalaCliApiException(
                "Received state doesn't match the requested one"
            )

        return True

    @staticmethod
    def _get_user_agent(data):
        for line in data:
            if line.lower().startswith("user-agent"):
                log.debug(line)
                break
        else:
            log.debug("No User-Agent")

    def _get_authorize_url(self, callback_port=None):
        """Gets OAuth2 URLs from Thabala."""
        try:
            response = requests.post(
                f"{self._api_base_url}/auth/authenticator-request",
                headers=self._headers,
                json={"browser_mode_redirect_port": callback_port},
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise_thabala_cli_api_exc(err, response.json())
        except Exception as err:
            raise_thabala_cli_api_exc(err)

        oauth2 = response.json().get("oauth2", dict())
        authorize_url = oauth2.get("authorize_url")

        return authorize_url

    def _get_tokens(self):
        """Get thabala access and refresh tokens"""
        try:
            response = requests.post(
                f"{self._api_base_url}/auth/token",
                headers=self._headers,
                json={
                    "grant_type": "authorization_code",
                    "code": self._code,
                },
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise_thabala_cli_api_exc(err, response.json())
        except Exception as err:
            raise_thabala_cli_api_exc(err)

        return response.json()
