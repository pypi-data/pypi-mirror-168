import json
import logging
import os
import socket
import time
import urllib.parse
import webbrowser
from typing import Dict

import requests

from thabala_cli.commands.utils.auth_password import AuthByPassword
from thabala_cli.commands.utils.auth_webbrowser import AuthByWebBrowser
from thabala_cli.commands.utils.profile import EXTERNAL_BROWSER_AUTHENTICATOR
from thabala_cli.commands.utils.profile import PASSWORD_AUTHENTICATOR
from thabala_cli.exceptions import ThabalaCliApiException
from thabala_cli.exceptions import ThabalaOperationException
from thabala_cli.utils.helpers import raise_thabala_cli_api_exc

log = logging.getLogger(__name__)


POLL_INTERVAL_SECONDS = 3


class RequestState:
    """
    Static class with service instance action request constants
    """

    REQUESTED = "requested"
    QUEUED = "queued"
    INPROGRESS = "inprogress"
    COMPLETED = "completed"
    FAILED = "failed"

    service_actions = (REQUESTED, QUEUED, INPROGRESS, COMPLETED, FAILED)


class ApiClient:
    def __init__(self, profile):
        self.profile = profile
        self.api_base_url = f"{self.profile['account_url']}/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self._access_token = None
        self._refresh_token = None

    @staticmethod
    def pretty_json(dic: Dict) -> str:
        return json.dumps(dic, indent=4, sort_keys=True)

    def _authenticate(self):
        """Login to the Thabala API"""
        authenticator = self.profile["authenticator"]

        if authenticator == PASSWORD_AUTHENTICATOR:
            auth_instance = AuthByPassword(
                self.api_base_url, self.profile["username"], self.profile["password"]
            )
        elif authenticator == EXTERNAL_BROWSER_AUTHENTICATOR:
            auth_instance = AuthByWebBrowser(self.api_base_url)
        else:
            raise ThabalaOperationException(f"Invalid authenticator: {authenticator}")

        self._access_token, self._refresh_token = auth_instance.authenticate()

    def _login_and_request(
        self, url: str, skip_login: bool = False, method: str = "GET", json_to_post=None
    ):
        if not skip_login:
            self._authenticate()

        try:
            response = requests.request(
                method,
                url,
                headers={
                    **self.headers,
                    **{
                        "Authorization": f"Bearer {self._access_token}",
                    },
                },
                json=json_to_post,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise_thabala_cli_api_exc(err, response.json())
        except Exception as err:
            raise_thabala_cli_api_exc(err)

        return response.json()

    def _poll_service_instance_request(
        self,
        service_instance_id: str,
        service_instance_request_id: str,
        state_message: str = None,
    ):
        """Periodically poll the service instance requests API endpoint until
        the request got completed."""
        log.info(f"Polling request status... {state_message or ''}")

        response_json = self._login_and_request(
            f"{self.api_base_url}/service-instances/{service_instance_id}/requests/{service_instance_request_id}"
        )

        state = response_json.get("result", {}).get("state")
        if state == RequestState.FAILED:
            print(ApiClient.pretty_json(response_json))
            raise ThabalaCliApiException(f"Service instance request failed.")
        if state == RequestState.COMPLETED:
            return response_json

        time.sleep(POLL_INTERVAL_SECONDS)
        return self._poll_service_instance_request(
            service_instance_id, service_instance_request_id, state_message=f"({state})"
        )

    def get_users(self, limit: int, offset: int):
        """Get list of users by the Thabala API"""
        params = {
            "limit": f"limit={limit}" if limit else "",
            "offset": f"offset={offset}" if offset else "",
        }
        response_json = self._login_and_request(
            f"{self.api_base_url}/users?{params['limit']}&{params['offset']}"
        )
        print(ApiClient.pretty_json(response_json))

    def get_service_instances(
        self, limit: int, offset: int, service_id: str, service_instance_id: str
    ):
        """Get list of service instances by the Thabala API"""
        if service_instance_id:
            if limit or offset or service_id:
                raise_thabala_cli_api_exc(
                    Exception(
                        f"Limit, offset and service_id parameters are not "
                        f"allowed to use together with service_instance_id"
                    )
                )

            endpoint_url = f"service-instances/{service_instance_id}"
        else:
            params = {
                "limit": f"limit={limit}" if limit else "",
                "offset": f"offset={offset}" if offset else "",
                "service_id": f"service_id={service_id}" if service_id else "",
            }
            endpoint_url = f"service-instances?{params['limit']}&{params['offset']}&{params['service_id']}"

        response_json = self._login_and_request(f"{self.api_base_url}/{endpoint_url}")
        print(ApiClient.pretty_json(response_json))

    def get_service_instance_users(
        self, limit: int, offset: int, username, service_instance_id: str
    ):
        """Get users of service instances"""
        params = {
            "limit": f"limit={limit}" if limit else "",
            "offset": f"offset={offset}" if offset else "",
            "username": f"username={username}" if username else "",
            "service_instance_id": f"service_instance_id={service_instance_id}"
            if service_instance_id
            else "",
        }
        endpoint_url = f"service-instances/users?{params['limit']}&{params['offset']}&{params['username']}&{params['service_instance_id']}"

        response_json = self._login_and_request(f"{self.api_base_url}/{endpoint_url}")
        print(ApiClient.pretty_json(response_json))

    def pause_service_instance(self, service_instance_id: str):
        """pause a specific service instance"""
        log.info("Requesting service instance to pause...")
        response_json = self._login_and_request(
            f"{self.api_base_url}/service-instances/{service_instance_id}/pause",
            method="POST",
        )
        service_instance_request_id = response_json.get("service_instance_request_id")
        if not service_instance_request_id:
            raise ThabalaCliApiException(
                f"Invalid response. service_instance_request_id not received."
            )

        response_json = self._poll_service_instance_request(
            service_instance_id, service_instance_request_id
        )
        print(ApiClient.pretty_json(response_json))

    def resume_service_instance(self, service_instance_id: str):
        """Resume a specific service instance"""
        log.info("Requesting service instance to resume...")
        response_json = self._login_and_request(
            f"{self.api_base_url}/service-instances/{service_instance_id}/resume",
            method="POST",
        )
        service_instance_request_id = response_json.get("service_instance_request_id")
        if not service_instance_request_id:
            raise ThabalaCliApiException(
                f"Invalid response. service_instance_request_id not received."
            )

        response_json = self._poll_service_instance_request(
            service_instance_id, service_instance_request_id
        )
        print(ApiClient.pretty_json(response_json))

    def get_health(self):
        """Get health of Thabala account"""
        response_json = self._login_and_request(
            f"{self.api_base_url}/health", skip_login=True
        )
        print(ApiClient.pretty_json(response_json))

    def get_infra(self, kind):
        """Get infrastructure as a code of the Thabala account"""
        response_json = self._login_and_request(f"{self.api_base_url}/infra")
        kinds = []
        if kind:
            kinds = kind.split(",")

        for component in response_json.get("result", []):
            c_kind = component["kind"]
            code = component["code"]

            if not kinds or c_kind in kinds:
                print("---")
                print(code)

    def post_infra(self, resource):
        """Post an infrastructure resource"""
        response_json = self._login_and_request(
            f"{self.api_base_url}/infra", method="POST", json_to_post=resource
        )

        service_instance_id = response_json.get("service_instance", {}).get("id")
        service_instance_request_id = response_json.get("service_instance_request_id")
        if service_instance_id and service_instance_request_id:
            self._poll_service_instance_request(
                service_instance_id, service_instance_request_id
            )

        return response_json

    def get_version(self):
        """Get version of Thabala account"""
        response_json = self._login_and_request(
            f"{self.api_base_url}/version", skip_login=True
        )
        print(ApiClient.pretty_json(response_json))
