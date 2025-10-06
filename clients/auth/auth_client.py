from httpx import Response, Client
from typing import Callable, TypeVar
from functools import wraps
from typing_extensions import ParamSpec
import logging
import allure


from utils.mapper import Mapper
from utils.assertions.schema import validate_json_schema
from clients.auth.auth_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
    RefreshResponseSchema,
)
from clients.base_schema import ApiResponse

P = ParamSpec("P")
R = TypeVar("R")

def auth(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        kwargs["auth"] = True
        return func(*args, **kwargs)
    return wrapper


class AuthClient:
    def __init__(self, client: Client):
        self.__clinet = client
        self.__access_token: str = None
        self.__refresh_token: str = None
        self.logger = logging.getLogger(__class__.__name__)

    def __set_auth_tokens(self, schema: LoginResponseSchema | RefreshResponseSchema):
        self.__access_token = schema.token.access_token
        self.__refresh_token = schema.token.refresh_token
            
    @allure.step("Send request to authenticate user (Login)")
    def login(self, request: LoginRequestSchema) -> ApiResponse[LoginResponseSchema]:
        try:
            response = self.__clinet.post(url="/login", json=Mapper.schema_to_dict(request))
            response.raise_for_status()
            validate_json_schema(response.json(), LoginResponseSchema.model_json_schema())
            response_schema = Mapper.json_to_schema(response.text, LoginResponseSchema)
            self.__set_auth_tokens(schema=response_schema)

            return ApiResponse(
                schema=response_schema,
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to login: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )
    
    @allure.step("Send request to refresh tokens")
    def refresh(self) -> ApiResponse[RefreshResponseSchema]:
        try:
            request = RefreshRequestSchema(
                refresh_token=self.__refresh_token
            )
            response = self.__clinet.post(url="/refresh", json=Mapper.schema_to_dict(request))
            response.raise_for_status()
            validate_json_schema(response.json(), RefreshResponseSchema.model_json_schema())
            response_schema = Mapper.json_to_schema(response.text, RefreshResponseSchema)
            self.__set_auth_tokens(schema=response_schema)

            return ApiResponse(
                schema=response_schema,
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to refresh: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )
        
    @property
    def access_token(self) -> str:
        return self.__access_token
    
    @property
    def auth_headers(self) -> dict:
        if not self.__access_token:
            raise Exception("Auth token doesn't exist in api client")
        
        headers = {
            "Authorization": f"Bearer {self.__access_token}"
        }
        return headers