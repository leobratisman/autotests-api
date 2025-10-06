from httpx import Client
import allure

from clients.base_client import BaseHTTPClient
from clients.auth.auth_client import AuthClient, auth
from clients.users.users_schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema, 
    GetCurrentUserResponseSchema,
    GetUserResponseSchema,
    UpdateUserRequestSchema,
    UpdateUserResponseSchema,
    UserSchema
)
from clients.base_schema import ApiResponse
from utils.mapper import Mapper
from utils.assertions.schema import validate_json_schema


class UsersClient(BaseHTTPClient):
    def __init__(self, client: Client, auth: AuthClient = None):
        super().__init__(client=client, auth=auth)
        self.__endpoint = "/users"
        self.__current_user: UserSchema | None = None

        if auth:
            response = self.get_current_user()
            self.__current_user = response.schema.user

    @property
    def current_user(self) -> UserSchema | None:
        return self.__current_user

    @allure.step("Create user")
    def create_user(self, request: CreateUserRequestSchema, **kwargs) -> ApiResponse[CreateUserResponseSchema]:
        try:
            response = self._post(
                endpoint=self.__endpoint,
                json=Mapper.schema_to_dict(request), 
                **kwargs
            )
            response.raise_for_status()
            validate_json_schema(response.json(), CreateUserResponseSchema.model_json_schema())
            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, CreateUserResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to create user: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )
    
    @auth
    @allure.step("Get current user")
    def get_current_user(self, **kwargs) -> ApiResponse[GetCurrentUserResponseSchema]:
        endpoint = f"{self.__endpoint}/me"
        try:
            response = self._get(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), GetCurrentUserResponseSchema.model_json_schema())
            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, GetCurrentUserResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to get current user: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Get user by ID")
    def get_user(self, user_id: str, **kwargs) -> ApiResponse[GetUserResponseSchema]:
        endpoint = f"{self.__endpoint}/{user_id}"
        try:
            response = self._get(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), GetUserResponseSchema.model_json_schema())
            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, GetUserResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to get user: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Update user by ID")
    def update_user(self, user_id: str, request: UpdateUserRequestSchema, **kwargs) -> ApiResponse[UpdateUserResponseSchema]:
        endpoint = f"{self.__endpoint}/{user_id}"
        try:
            response = self._patch(
                endpoint=endpoint, 
                json=Mapper.schema_to_dict(request, exclude_none=True), 
                **kwargs
            )
            response.raise_for_status()
            validate_json_schema(response.json(), UpdateUserRequestSchema.model_json_schema())
            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, UpdateUserResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to update user: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Delete user by ID")
    def delete_user(self, user_id: str, **kwargs) -> ApiResponse:
        endpoint = f"{self.__endpoint}/{user_id}"
        try:
            response = self._delete(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            return ApiResponse(
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to delete user: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )
