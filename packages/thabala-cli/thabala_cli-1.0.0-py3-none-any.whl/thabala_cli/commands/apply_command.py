"""Apply command"""
from thabala_cli.commands.utils.infra_code import InfraCode
from thabala_cli.commands.utils.profile import get_profile


def apply(args):
    """Apply infrastructure component"""
    profile = get_profile(args)
    infra_code = InfraCode(profile)

    infra_code.apply_yaml(args.file)
