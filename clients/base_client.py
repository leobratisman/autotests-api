import allure
from httpx import (
    Client, 
    QueryParams,
    Response,
    URL
)
from httpx._types import RequestData, RequestFiles
from typing import Any
from utils.logger import get_logger

from clients.auth.auth_client import AuthClient


class BaseHTTPClient:
    def __init__(self, client: Client, auth: AuthClient = None):
        self.__client = client
        self.__auth = auth
        self.logger = get_logger(__class__.__name__)

    def __prepare_headers(self, headers: dict, auth: bool) -> dict:
        headers = headers.copy() if headers else {}
        if auth and self.__auth:
            headers.update(self.__auth.auth_headers)
        return headers

    @allure.step("Send GET request to {endpoint}")
    def _get(
        self, 
        endpoint: URL | str, 
        params: QueryParams = None,
        auth: bool = False,
        **kwargs
    ) -> Response:
        if params is None:
            params = {}

        headers: dict = self.__prepare_headers(headers=kwargs.pop("headers", {}), auth=auth)
        return self.__client.get(url=endpoint, params=params, headers=headers, **kwargs)
    
    @allure.step("Send POST request to {endpoint}")
    def _post(
        self,
        endpoint: URL | str,
        json: Any | None = None,
        data: Any | RequestData | None = None,
        files: RequestFiles | None = None,
        auth: bool = False,
        **kwargs
    ) -> Response:
        headers: dict = self.__prepare_headers(headers=kwargs.pop("headers", {}), auth=auth)
        return self.__client.post(url=endpoint, json=json, data=data, files=files, headers=headers, **kwargs)

    @allure.step("Send PATCH request to {endpoint}")
    def _patch(
        self,
        endpoint: URL | str,
        json: Any | None = None,
        auth: bool = False,
        **kwargs
    ) -> Response:
        headers: dict = self.__prepare_headers(headers=kwargs.pop("headers", {}), auth=auth)
        return self.__client.patch(url=endpoint, json=json, headers=headers, **kwargs)
    
    @allure.step("Send DELETE request to {endpoint}")
    def _delete(
        self,
        endpoint: URL | str,
        auth: bool = False,
        **kwargs
    ) -> Response:
        headers: dict = self.__prepare_headers(headers=kwargs.pop("headers", {}), auth=auth)
        return self.__client.delete(url=endpoint, headers=headers, **kwargs)
    