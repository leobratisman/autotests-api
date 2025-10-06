from httpx import Response
import allure

from clients.base_client import BaseHTTPClient
from clients.auth.auth_client import auth

from clients.files.files_schema import (
    GetFileResponseSchema,
    CreateFileRequestSchema,
    CreateFileResponseSchema
)
from clients.base_schema import ApiResponse
from utils.mapper import Mapper
from utils.assertions.schema import validate_json_schema


class FilesClient(BaseHTTPClient):
    def __init__(self, client, auth = None):
        super().__init__(client, auth)
        self.__endpoint = "/files"

    @auth
    @allure.step("Get file by ID")
    def get_file(self, file_id: str, **kwargs) -> ApiResponse[GetFileResponseSchema]:
        endpoint = f"{self.__endpoint}/{file_id}"
        try:
            response = self._get(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), GetFileResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, GetFileResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to get file: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Create file")
    def create_file(self, request: CreateFileRequestSchema, **kwargs) -> ApiResponse[CreateFileResponseSchema]:
        try:
            response = self._post(
                endpoint=self.__endpoint,
                data=Mapper.schema_to_dict(request, exclude={"upload_file"}),
                files={"upload_file": open(request.upload_file, "rb")},
                **kwargs
            )
            response.raise_for_status()
            validate_json_schema(response.json(), CreateFileResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, CreateFileResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to create file: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )


    @auth
    @allure.step("Delete file by ID")
    def delete_file(self, file_id: str, **kwargs) -> ApiResponse:
        endpoint = f"{self.__endpoint}/{file_id}"
        try:
            response = self._delete(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            return ApiResponse(
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to delete file: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )