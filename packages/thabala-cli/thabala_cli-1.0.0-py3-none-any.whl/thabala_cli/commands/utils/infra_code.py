import logging

import yaml

from thabala_cli.commands.utils.api_client import ApiClient
from thabala_cli.exceptions import ThabalaCliInfraCodeException

log = logging.getLogger(__name__)


VALID_KINDS = ["Authenticator", "Users", "ServiceInstance"]


class InfraCode:
    def __init__(self, profile):
        self.api_client = ApiClient(profile)

        InfraCode.kind_appliers = {
            "Authenticator": self._apply_authenticator,
            "Users": self._apply_users,
            "ServiceInstance": self._apply_service_instance,
        }

    def _apply_authenticator(self, resource):
        log.info(f"Applying authenticator...")
        return self.api_client.post_infra(resource)

    def _apply_users(self, resource):
        log.info(f"Applying users...")
        return self.api_client.post_infra(resource)

    def _apply_service_instance(self, resource):
        service_id = resource.get("instance", {}).get("service_id")
        service_instance_name = resource.get("instance", {}).get("name")
        log.info(
            f"Applying service instance... ({service_id}: {service_instance_name})"
        )
        return self.api_client.post_infra(resource)

    @staticmethod
    def _validate_resource(resource):
        kind = resource.get("kind")
        if not kind:
            raise ThabalaCliInfraCodeException(f"Resource kind not found in the YAML.")
        if kind not in InfraCode.kind_appliers.keys():
            raise ThabalaCliInfraCodeException(f"Invalid resource kind {kind}")

    @staticmethod
    def _load_yaml(yaml_file):
        resources = []
        try:
            with open(yaml_file, "r") as f:
                try:
                    resources_yaml = yaml.load_all(f, Loader=yaml.SafeLoader)
                    for resource_yaml in resources_yaml:
                        InfraCode._validate_resource(resource_yaml)
                        resources.append(resource_yaml)
                except yaml.YAMLError as exc:
                    raise ThabalaCliInfraCodeException(exc)
        except OSError as exc:
            raise ThabalaCliInfraCodeException(exc)

        return resources

    @staticmethod
    def apply_yaml(yaml_file):
        resources = InfraCode._load_yaml(yaml_file)
        result = []
        for resource in resources:
            kind = resource["kind"]
            result.append(InfraCode.kind_appliers[kind](resource))

        print(ApiClient.pretty_json(result))
