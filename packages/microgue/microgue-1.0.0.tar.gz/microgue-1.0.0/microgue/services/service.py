import aiohttp
import asyncio
import json
import logging
import requests
import traceback
from collections import OrderedDict
from ..constants.error_constants import ErrorConstants
from ..utils import mask_fields_in_data

logger = logging.getLogger("microgue")


class Service:
    class Response:
        def __init__(self, status_code=400, headers={}, cookies={}, data={}):
            self.status_code = status_code
            self.headers = headers
            self.cookies = cookies
            self.data = data

    def __init__(self, *args, **kwargs):
        self.request_base_url = ""
        self.mask_request_headers_fields = []
        self.mask_request_data_fields = []

    def invoke(
            self,
            request_url="",
            request_parameters={},
            request_method="GET",
            request_headers={},
            request_cookies={},
            request_data={},
            request_files={},
            verify_ssl=True
    ):
        logger.debug(f"########## {self.__class__.__name__} Invoke ##########")
        logger.debug(f"request url: {request_url}")
        logger.debug(f"request method: {request_method}")
        logger.debug(f"request headers: {mask_fields_in_data(request_headers, self.mask_request_headers_fields)}")
        logger.debug(f"request cookies: {request_cookies}")
        logger.debug(f"request data: {mask_fields_in_data(request_data, self.mask_request_data_fields)}")

        # open all files before sending them
        opened_request_files = OrderedDict()
        for key, file in request_files.items():
            opened_request_files[key] = open(file, "rb")

        try:
            requests_response = requests.request(
                url=self.request_base_url + request_url,
                params=request_parameters,
                method=request_method,
                headers=request_headers,
                cookies=request_cookies,
                data=request_data,
                files=opened_request_files,
                verify=verify_ssl
            )

            response_status_code = requests_response.status_code
            response_headers = dict(requests_response.headers)
            response_cookies = dict(requests_response.cookies)

            try:
                response_data = requests_response.json()
            except:
                response_data = requests_response.text

            logger.debug(f"########## {self.__class__.__name__} Invoke Response")
            logger.debug(f"response status code: {response_status_code}")
            logger.debug(f"response headers: {response_headers}")
            logger.debug(f"response cookies: {response_cookies}")
            logger.debug(f"response data: {response_data}")

        except Exception as e:
            logger.error(f"########## {self.__class__.__name__} Invoke Error")
            logger.error(f"{e.__class__.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            response_status_code = 500
            response_headers = {}
            response_cookies = {}
            response_data = {"error": ErrorConstants.App.INTERNAL_SERVER_ERROR}

        return self.Response(
            status_code=response_status_code,
            headers=response_headers,
            cookies=response_cookies,
            data=response_data
        )
