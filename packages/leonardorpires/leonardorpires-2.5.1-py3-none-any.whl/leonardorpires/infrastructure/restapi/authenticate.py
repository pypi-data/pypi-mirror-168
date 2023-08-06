import json
from typing import Optional

from requests import PreparedRequest, Request, Session


class RestApiAuthenticate(object):
    """
    This class intends to authenticate a REST API request

    :param auth_credentials: the auth_credentials dictionary
    :type auth_credentials: optional, dict

    :param session: the requests Session
    :type session: optional, requests.Session
    """

    def __init__(
        self,
        auth_credentials: Optional[dict] = None,
        session: Optional[Session] = None,
    ):
        self.auth_credentials = auth_credentials
        self.session = session or Session()

    def build(self, prepped: PreparedRequest):
        if self.auth_credentials:
            data = self.auth_credentials.get("data")
            BasicAuth(
                auth_type=self.auth_credentials.get("auth_type"),
                username=data.get("username", None),
                password=data.get("password", None),
                username_label=data.get("username_label", None),
                password_label=data.get("password_label", None),
            ).build(prepped=prepped)
            OAuthTwo(
                auth_type=self.auth_credentials.get("auth_type"),
                auth_token_label=data.get("auth_token_label", None),
                auth_token_mapping=data.get("auth_token_mapping", None),
                auth_url=data.get("auth_url", None),
                auth_method=data.get("auth_method", None),
                auth_data=data.get("auth_data", None),
                auth_headers=data.get("auth_headers", None),
                session=self.session,
            ).build(prepped=prepped)
        return prepped


class BasicAuth(object):
    """
    This class intends to authenticate a basic login and password auth at a REST API request body

    :param auth_type: the string containing the auth type
    :type auth_type: required, string

    :param username: the username information as a string
    :type username: optional, string

    :param password: the password information as a string
    :type password: optional, string

    :param username_label: the username label information as a string
    :type username_label: optional, string

    :param password_label: the password label information as a string
    :type password_label: optional, string
    """

    def __init__(
        self,
        auth_type: str,
        username: str,
        password: str,
        username_label: str,
        password_label: str,
    ):
        self.auth_type = auth_type
        self.username = username
        self.password = password
        self.username_label = username_label
        self.password_label = password_label

    def build(self, prepped: PreparedRequest):
        """
        This method intends to authenticate a REST API request using basic auth

        :param prepped: the prepped request to be authenticated
        :type prepped: required, requests.PreparedRequest
        """
        if (
            self.auth_type == "basic"
            and self.username
            and self.password
            and self.username_label
            and self.password_label
        ):
            auth_dict = {
                self.username_label: self.username,
                self.password_label: self.password,
            }
            prepped.body = (
                json.dumps(json.loads(prepped.body).update(auth_dict))
                if prepped.body
                else json.dumps(auth_dict)
            )


class OAuthTwo(object):
    """
    This class intends to authenticate using oauth2 at a REST API request body

    :param auth_type: the string containing the auth type
    :type auth_type: required, string

    :param auth_token_label: the authorization token label information as a string
    :type auth_token_label: optional, string

    :param auth_token_mapping: the authorization token mapping information as a list. i.e.: ["data"]
    :type auth_token_mapping: optional, string

    :param auth_url: the authorization url information as a string
    :type auth_url: optional, string

    :param auth_method: the authorization method information as a string
    :type auth_method: optional, string

    :param auth_data: the authorization data information as a dictionary
    :type auth_data: optional, dict

    :param auth_headers: the authorization headers information as a dictionary
    :type auth_headers: optional, dict

    :param session: the requests Session
    :type session: optional, requests.Session
    """

    def __init__(
        self,
        auth_type: str,
        auth_token_label: Optional[str] = None,
        auth_token_mapping: Optional[list] = None,
        auth_url: Optional[str] = None,
        auth_method: Optional[str] = None,
        auth_data: Optional[dict] = None,
        auth_headers: Optional[dict] = None,
        session: Optional[Session] = None,
    ):
        self.auth_type = auth_type
        self.auth_token_label = auth_token_label
        self.auth_token_mapping = auth_token_mapping
        self.auth_url = auth_url
        self.auth_method = auth_method
        self.auth_data = json.dumps(auth_data)
        self.auth_headers = auth_headers
        self.session = session or Session()

    def get_value_using_list(self, data, key_list):
        return (
            self.get_value_using_list(data[key_list[0]], key_list[1:])
            if key_list
            else data
        )

    def build(self, prepped: PreparedRequest):
        """
        This method intends to authenticate a REST API request using OAuth2

        :param prepped: the prepped request to be authenticated
        :type prepped: required, requests.PreparedRequest
        """
        if (
            self.auth_type == "oauth2"
            and self.auth_method
            and self.auth_url
            and self.auth_token_mapping
            and self.auth_token_label
        ):
            auth_req = Request(
                method=self.auth_method,
                url=self.auth_url,
                data=self.auth_data,
                headers=self.auth_headers,
            )
            auth_resp = self.session.send(auth_req.prepare())
            if auth_resp.status_code == 200:
                auth_token = self.get_value_using_list(
                    json.loads(auth_resp.text), self.auth_token_mapping
                )
                auth_dict = {self.auth_token_label: auth_token}
                prepped.headers.update(auth_dict)
