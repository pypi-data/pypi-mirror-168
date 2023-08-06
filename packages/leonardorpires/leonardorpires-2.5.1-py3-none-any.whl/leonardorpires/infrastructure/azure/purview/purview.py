import json
from json import JSONDecodeError
from typing import Dict, List, Union

import requests
from requests import Response

from pyiris.infrastructure.azure.authentication.api import Api
from pyiris.infrastructure.common.config import get_key


class Purview(object):
    """
    Provides communication between your application and the Azure Purview server with your entities and type definitions.
    :param auth: The method of authentication.
    :type authentication: :class:`~pyiris.infrastructure.azure.authentication.api.Api`
    """

    def __init__(self, auth: Dict):
        self.headers = Purview.build_headers(auth)

    def _handle_response(self, response: Response) -> dict:
        """
        Safely handle an Purview Response and return the results if valid.
        :param response: The response from the request method.
        :type response: :class: Response
        :return: A dict containing the results ir RequestException.
        :type: dict
        """

        try:
            result = json.loads(response.text)
            response.raise_for_status()
        except JSONDecodeError:
            raise ValueError("Error in parsing: {}".format(response.text))
        except Exception:
            raise requests.RequestException(response.text)

        return result

    def create_entities(self, body: Dict) -> Union[dict, requests.RequestException]:
        """
        Create entities to your Purview backed Data Catalog.
        :param body: The body of entities you want to create. Supports a dict of purview entities.
        :type body: dict
        :return: The results of your bulk entity create.
        :rtype: dict
        """

        endpoint = "https://{pvw_account_name}.catalog.purview.azure.com/api/atlas/v2/entity/bulk".format(
            pvw_account_name=get_key("IrisPurviewAccountName")
        )

        response = requests.post(
            url=endpoint, data=json.dumps(body), headers=self.headers
        )

        return self._handle_response(response)

    def get_glossary_terms(self) -> Union[dict, List[Dict], requests.RequestException]:
        """
        Get all glossary terms to your Purview backed Data Catalog.
        :return: The results of your glossary terms.
        :rtype: dict
        """

        endpoint = "https://{pvw_account_name}.catalog.purview.azure.com/api/atlas/v2/glossary/name/Glossary/terms".format(
            pvw_account_name=get_key("IrisPurviewAccountName")
        )
        response = requests.get(url=endpoint, headers=self.headers)
        return self._handle_response(response)

    def get_entity_by_type(self, body):
        endpoint = "https://purview-iris-catalogo.purview.azure.com/catalog/api/search/query?api-version=2021-05-01-preview"
        response = requests.post(
            url=endpoint, data=json.dumps(body), headers=self.headers
        )
        return self._handle_response(response)

    def delete_entity(self, guid):
        endpoint = "https://{pvw_account_name}.catalog.purview.azure.com/api/atlas/v2/entity/guid/{guid}".format(
            pvw_account_name=get_key("IrisPurviewAccountName"), guid=guid
        )
        response = requests.delete(url=endpoint, headers=self.headers)
        return self._handle_response(response)

    @staticmethod
    def build_headers(auth: Dict) -> Dict:
        """
        Build the current access token or refreshes the token if it has expired.
        :return: The authorization headers.
        :rtype: dict
        """
        return {
            "Authorization": "Bearer {access_token}".format(
                access_token=auth["access_token"]
            ),
            "Content-Type": "application/json",
        }

    @staticmethod
    def build():
        """
        Build an Azure Purview Instance with Authentication.
        :return: Purview class instance.
        :rtype: :class:`~pyiris.infrastructure.azure.purview.purview.Purview`
        """
        api_auth = Api(
            resource="https://purview.azure.net",
            subscription_id=get_key("IrisPurviewSubscriptionId"),
            tenant_id=get_key("IrisPurviewTenantId"),
            client_id=get_key("IrisPurviewClientId"),
            client_secret=get_key("IrisPurviewClientSecret"),
        )

        return Purview(auth=api_auth())
