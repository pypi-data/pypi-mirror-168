from typing import Optional, Union

from pyspark.sql import DataFrame
from requests import Request, Session

from pyiris.infrastructure import Spark
from pyiris.infrastructure.restapi.authenticate import RestApiAuthenticate
from pyiris.infrastructure.restapi.response_data import ResponseData
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.extract.readers.reader import Reader

logger = Logger(__name__)


class RestApiReader(Reader):
    """
    This class intends to make a request (or multiple when paginated) to a REST API and parse the results

    :param url: the requested url
    :type url: required, string

    :param method: the request method
    :type method: required, string

    :param rest_authenticate: the RestApiAuthenticate object
    :type rest_authenticate: required, pyiris.infrastructure.restapi.authenticate.RestApiAuthenticate

    :param response_schema: the data response schema as a dictionary
    :type response_schema: required, dict

    :param data_response_mapping: the data location within the response schema as a list
    :type data_response_mapping: required, list

    :param pagination_options: the pagination options as a dictionary
    :type pagination_options: optional, dict

    :param response_data: the ResponseData object
    :type response_data: optional, pyiris.infrastructure.restapi.response_data.ResponseData

    :param body: the main request body as a dictionary
    :type body: optional, dict

    :param headers: the main request headers as a dictionary
    :type headers: optional, dict

    :param engine: the Spark session
    :type engine: optional, pyiris.infrastructure.spark.spark.Spark
    """

    def __init__(
        self,
        api_id: str,
        url: str,
        method: str,
        response_schema: dict,
        data_response_mapping: list,
        rest_authenticate: Optional[RestApiAuthenticate] = None,
        pagination_options: Optional[dict] = None,
        response_data: Optional[ResponseData] = None,
        body: Optional[dict] = None,
        headers: Optional[dict] = None,
        engine: Optional[Spark] = None,
    ):
        super().__init__(api_id)
        self.url = url
        self.method = method
        self.rest_authenticate = rest_authenticate or RestApiAuthenticate()
        self.response_schema = response_schema
        self.data_response_mapping = data_response_mapping
        self.pagination_options = pagination_options or {}
        self.body = body
        self.headers = headers
        self.engine = engine or Spark()
        self.base_request = Request(
            self.method, self.url, data=self.body, headers=self.headers
        )

        self.session = Session()
        self.base_request = self.rest_authenticate.build(self.base_request)

        self.response_data = response_data or ResponseData(
            data_response_mapping=self.data_response_mapping,
            options=self.pagination_options,
            base_request=self.base_request,
            session=self.session,
        )

    @logger.log_decorator
    def consume(self, **kwargs) -> Union[DataFrame, ValueError]:
        """
        This method intends to return the api response as a spark dataframe

        :return: the intended dataframe
        :rtype: pyspark.sq.DataFrame
        """
        return self.engine.parse_dict_list_to_dataframe(
            data=self.response_data.get_json(), schema=self.response_schema
        )
