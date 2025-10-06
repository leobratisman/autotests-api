from httpx import Client
from config import settings
from functools import lru_cache

from clients.auth.auth_client import AuthClient
from clients.base_client import BaseHTTPClient
from clients.users.users_client import UsersClient
from clients.files.files_client import FilesClient
from clients.courses.courses_client import CoursesClient
from clients.exercises.exercises_client import ExercisesClient

from clients.auth.auth_schema import (
    LoginRequestSchema, 
    LoginResponseSchema
)
from clients.base_schema import ApiResponse, BaseSchema
from clients.event_hooks import curl_attach_to_allure_event_hook, log_request_event_hook, log_response_event_hook


def get_http_client() -> Client:
    return Client(
        base_url=settings.API_BASE_URL, 
        timeout=settings.TIMEOUT, 
        event_hooks={
            "request": [curl_attach_to_allure_event_hook, log_request_event_hook],
            "response": [log_response_event_hook]
        }
    )

def get_http_client_for_auth() -> Client:
    return Client(
        base_url=settings.API_AUTH_URL, 
        timeout=settings.TIMEOUT, 
        event_hooks={
            "request": [curl_attach_to_allure_event_hook, log_request_event_hook],
            "response": [log_response_event_hook]
        }
    )

def get_base_client() -> BaseHTTPClient:
    return BaseHTTPClient(client=get_http_client())

# ------------------------------ Auth ---------------------------------

class GetAuthClientSchema(BaseSchema):
    client: AuthClient
    response: ApiResponse[LoginResponseSchema]

    model_config = {"arbitrary_types_allowed": True}

@lru_cache(maxsize=None)
def get_auth_client(creds: LoginRequestSchema) -> GetAuthClientSchema:
    client = AuthClient(client=get_http_client_for_auth())
    response = client.login(request=creds)
    return GetAuthClientSchema(
        client=client,
        response=response
    )

# ------------------------------ Users ---------------------------------

def get_public_users_client() -> UsersClient:
    return UsersClient(client=get_http_client())

def get_private_users_client(auth: AuthClient) -> UsersClient:
    return UsersClient(client=get_http_client(), auth=auth)

# ------------------------------ Files ---------------------------------

def get_files_client(auth: AuthClient) -> FilesClient:
    return FilesClient(client=get_http_client(), auth=auth)

# ------------------------------ Courses ---------------------------------

def get_courses_client(auth: AuthClient) -> CoursesClient:
    return CoursesClient(client=get_http_client(), auth=auth)

# ------------------------------ Exercises ---------------------------------

def get_exercises_client(auth: AuthClient) -> ExercisesClient:
    return ExercisesClient(client=get_http_client(), auth=auth)