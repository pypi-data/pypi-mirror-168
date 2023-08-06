from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext


class SharePointConnection(object):
    """
    This class intends to make a connection with SharePoint Site.
    """

    @staticmethod
    def build(client_id: str, client_secret: str, url: str) -> ClientContext:
        """
        This method is responsible for building authentication with SharePoint and returning Client Context object.

        :param client_id: client id for Azure app registration
        :type client_id: str

        :param client_secret: client secret for Azure app registration
        :type client_secret: str

        :param url: SharePoint authority url.
        :type url: str

        """
        context_authentication = AuthenticationContext(url)
        context_authentication.acquire_token_for_app(
            client_id=client_id, client_secret=client_secret
        )
        return ClientContext(url, context_authentication)
