from azure.keyvault.secrets import SecretClient


class KeyVault(object):
    """
    This class is responsible for getting, through an Key Vault Authenticator object, the given key.

    :param client: an authentication object
    :type client: azure.keyvault.secrets.SecretClient
    """

    def __init__(self, client: SecretClient):
        self.client = client

    def get(self, key) -> str:
        """
        This method intends to return a secret based on a given key.
        """
        secret = self.client.get_secret(key)
        return secret.value

    @staticmethod
    def build(authenticator):
        return KeyVault(client=authenticator.get_client())
