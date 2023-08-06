from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient


class KeyVaultAuthenticator(object):
    """
    This class intends to create an authentication object through an app registration to perform a Microsoft Key Vault
    secret requisition.

    :param tenant_id: the app registration tenant id credential
    :type tenant_id: String

    :param client_id: the app registration client id credential
    :type client_id: String

    :param client_secret: the app registration client secret
    :type client_secret: String

    :param key_vault_name: the name os the Microsoft Key Vault resource
    :type key_vault_name: String
    """

    def __init__(self, tenant_id, client_id, client_secret, key_vault_name):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.key_vault_name = key_vault_name

    def get_client(self) -> SecretClient:
        """
        This method is responsible for making the Key Vault authentication.

        :return: an Key Vault client
        :rtype: azure.keyvault.secrets.SecretClient
        """
        secret_client = SecretClient(
            vault_url=self.build_url(),
            credential=ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret,
            ),
        )

        return secret_client

    def build_url(self) -> str:
        """
        This method is responsible for returning a Key Vault authentication url in the format
        "https://{key_vault_name}.vault.azure.net/"

        :return: a Key Vault authentication url
        :rtype: String
        """
        return "https://{key_vault_name}.vault.azure.net/".format(
            key_vault_name=self.key_vault_name
        )
