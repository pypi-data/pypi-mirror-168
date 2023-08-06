import json

from requests import Request, Session


class ResponseData(object):
    """
    This class intends to get the data as json from the API response (or responses, when paginated).

    :param data_response_mapping: the data location within the response schema as a list
    :type data_response_mapping: required, list

    :param options: the pagination options as a dictionary
    :type options: required, dict

    :param base_request: the base request.
    :type base_request: required, requests.Request

    :param session: the requests Session
    :type session: optional, requests.Session
    """

    def __init__(
        self,
        data_response_mapping: list,
        options: dict,
        base_request: Request,
        session: Session,
    ):
        self.data_response_mapping = data_response_mapping
        self.options = options
        self.base_request = base_request
        self.session = session

    def get_value_using_list(self, data, key_list):
        return (
            self.get_value_using_list(data[key_list[0]], key_list[1:])
            if key_list
            else data
        )

    def get_json(self):
        if self.get_json_response_with_pagination():
            return self.get_json_response_with_pagination()
        if self.get_json_response_without_pagination():
            return self.get_json_response_without_pagination()

    def get_json_response_with_pagination(self) -> json:
        if (
            self.options.get("number_of_pages_mapping")
            and self.options.get("current_page_mapping")
            and self.options.get("current_page_label")
        ):
            response = self.session.send(self.base_request.prepare())
            max_page = self.get_value_using_list(
                json.loads(response.text),
                self.options.get("number_of_pages_mapping"),
            )
            start_page = self.get_value_using_list(
                json.loads(response.text), self.options.get("current_page_mapping")
            )
            request_list = list()
            self.base_request.params = {
                self.options.get("current_page_label"): start_page
            }
            request_list.append(self.base_request)
            page = start_page
            while page < max_page:
                page += 1
                request = Request(
                    url=self.base_request.url,
                    method=self.base_request.method,
                    headers=self.base_request.headers,
                    params={self.options.get("current_page_label"): page},
                )
                request_list.append(request)
            response_list = []
            for page_request in request_list:
                response = self.session.send(page_request.prepare())
                if response.status_code == 200:
                    response_list += self.get_value_using_list(
                        json.loads(response.text), self.data_response_mapping
                    )
                else:
                    raise Exception(response)
            return response_list

    def get_json_response_without_pagination(self) -> json:
        if not self.options:
            response = self.session.send(self.base_request.prepare())
            if response.status_code == 200:
                response_json = self.get_value_using_list(
                    json.loads(response.text), self.data_response_mapping
                )
                return response_json
            else:
                raise Exception(response)
