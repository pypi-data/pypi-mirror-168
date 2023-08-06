import json
import logging

import requests


class Api(object):
    """
    This class provides communication between your application and the Azure Authentication API to generate a bearer token to connect to Azure Resources.

    :param resource: Azure resource that you want to connect
    :type: str

    :param subscription_id: azure subscription id
    :type: str

    :param tenant_id: tenant id for app registration
    :type: str

    :param client_id: client id for app registration
    :type: str

    :param client_secret: client secret for app registration
    :type: str

    """

    def __init__(
        self,
        resource: str,
        subscription_id: str,
        tenant_id: str,
        client_id: str,
        client_secret: str,
    ):
        self.resource = resource
        self.subscription_id = subscription_id
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

    def __call__(self):
        """
        Call Azure authentication when the API class is instantiated

        :return: A dict containing the authentication result.
        :rtype: dict

        """
        auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

        auth_body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "resource": self.resource,
            "grant_type": "client_credentials",
        }

        endpoint = "https://login.microsoftonline.com/{tenent_id}/oauth2/token".format(
            tenent_id=self.tenant_id
        )

        response = requests.post(url=endpoint, headers=auth_headers, data=auth_body)
        if response.status_code in (200, 201):
            logging.info("Authenticate with successfully.")
            return json.loads(response.text)
        else:
            logging.info(
                "Error when try to Authenticate. Message: {message}".format(
                    message=response.text
                )
            )
            raise Exception(response.text)
