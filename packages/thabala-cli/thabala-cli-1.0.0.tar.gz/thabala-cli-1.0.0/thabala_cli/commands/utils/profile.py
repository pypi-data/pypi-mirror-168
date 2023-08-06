"""Profile"""
from thabala_cli.configuration import conf
from thabala_cli.exceptions import ThabalaCliConfigException

PASSWORD_AUTHENTICATOR = "PASSWORD"
EXTERNAL_BROWSER_AUTHENTICATOR = "EXTERNALBROWSER"

AUTHENTICATORS = [
    PASSWORD_AUTHENTICATOR,
    EXTERNAL_BROWSER_AUTHENTICATOR,
]


def validate_profile(profile):
    if not profile.get("account_url"):
        raise ThabalaCliConfigException(f"Invalid profile. Missing account_url")
    if not profile.get("authenticator"):
        raise ThabalaCliConfigException(f"Invalid profile. Missing authenticator")

    #  Authenticator needs to be a known one
    if profile.get("authenticator") not in AUTHENTICATORS:
        raise ThabalaCliConfigException(
            f"Invalid authenticator: {profile.get('authenticator')}"
        )

    # Validate properties for the password authenticator
    if profile.get("authenticator") == PASSWORD_AUTHENTICATOR:
        if not profile.get("username"):
            raise ThabalaCliConfigException(f"Invalid profile. Missing username")
        if not profile.get("password"):
            raise ThabalaCliConfigException(f"Invalid profile. Missing password")


def get_profile(args):
    profile_name = (
        f"profile {args.profile}" if args.profile != "default" else args.profile
    )
    profile = {
        "account_url": conf.get(profile_name, "account_url"),
        "authenticator": conf.get(profile_name, "authenticator"),
        "username": conf.get(profile_name, "username"),
        "password": conf.get(profile_name, "password"),
    }

    validate_profile(profile)
    return profile
