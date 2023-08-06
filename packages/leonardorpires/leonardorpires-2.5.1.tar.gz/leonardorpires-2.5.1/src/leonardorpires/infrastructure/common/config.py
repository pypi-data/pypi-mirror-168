import configparser
import os

from pyiris.infrastructure.azure.authentication.key_vault import KeyVaultAuthenticator
from pyiris.infrastructure.azure.key_vault.key_vault import KeyVault

environment = os.environ.get("ENVIRONMENT", "TEST")
_config = configparser.ConfigParser()
_config.read(os.path.dirname(__file__) + "/../../config/config.ini")


def get_key(key: str) -> str:
    """
    This function is responsible for managing the credentials sources when called. The sources available, in preference,
    order are: environment variable, Microsoft Key Vault and config.ini file.

    :param key: the solicited key
    :type key: String

    :return: the key solicited from the available sources
    :rtype: String

    :raises: ValueError -- "Secret was not found or couldn't be gotten from Key Vault. Secret:" + key
    """
    env_value = os.environ.get(key)
    if not env_value:
        try:
            authenticator = KeyVaultAuthenticator(
                key_vault_name=os.environ.get("KEY_VAULT_NAME"),
                tenant_id=os.environ.get("PYIRIS_TENANT_ID"),
                client_id=os.environ.get("PYIRIS_CLIENT_ID"),
                client_secret=os.environ.get("PYIRIS_SECRET"),
            )
            key_vault = KeyVault.build(authenticator=authenticator)
            key_vault_secret = key_vault.get(set_private_key(key))
            return key_vault_secret
        except Exception:
            key_vault_secret = None
        if not key_vault_secret:
            try:
                config_value = _config[environment][set_private_key(key=key)]
                return config_value
            except ValueError:
                raise ValueError(
                    "Secret was not found or couldn't be gotten from Key Vault. Secret:"
                    + key
                )
    else:
        return env_value


def set_private_key(key: str) -> str:
    """
    This function set the key name accord of the environment variable "ENVIRONMENT_PERMISSION". If it is equal "PUBLIC"
    the key name is not change. Else, if the variable is equal "PRIVATE", the string "Private" os added for the key
    name.

    :return: the name of the key
    :rtype: String
    """
    if os.environ.get("ENVIRONMENT_PERMISSION") == "PRIVATE":
        key = "{key}Private".format(key=key)
    return key
