import pytest

from clients.deps import (
    get_auth_client,
    AuthClient as AuthClientSchema
)
from clients.auth.auth_client import AuthClient
from clients.auth.auth_schema import LoginRequestSchema


@pytest.fixture(scope="function")
def auth_client(user_function) -> AuthClient:
    request = LoginRequestSchema(email=user_function.email, password=user_function.password)
    return get_auth_client(creds=request).client

@pytest.fixture(scope="function")
def auth_client_with_login_request_info(user_function) -> AuthClientSchema:
    request = LoginRequestSchema(email=user_function.email, password=user_function.password)
    return get_auth_client(creds=request)