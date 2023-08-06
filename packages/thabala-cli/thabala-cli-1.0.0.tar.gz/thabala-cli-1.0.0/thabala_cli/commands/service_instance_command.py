"""Service instance command"""
from thabala_cli.commands.utils.api_client import ApiClient
from thabala_cli.commands.utils.profile import get_profile


def pause(args):
    """Get users"""
    api_client = ApiClient(get_profile(args))
    api_client.pause_service_instance(args.service_instance_id)


def resume(args):
    """Get users"""
    api_client = ApiClient(get_profile(args))
    api_client.resume_service_instance(args.service_instance_id)
