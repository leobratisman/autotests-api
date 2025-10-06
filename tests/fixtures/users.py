import pytest
from pydantic import BaseModel, EmailStr

from clients.deps import (
    get_public_users_client,
    get_private_users_client
)
from clients.users.users_client import UsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from clients.base_schema import ApiResponse


class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: ApiResponse[CreateUserResponseSchema]

    @property
    def email(self) -> EmailStr:
        return self.request.email
    
    @property
    def password(self) -> str:
        return self.request.password


@pytest.fixture(scope="function")
def users_public_client() -> UsersClient:
    return get_public_users_client()

@pytest.fixture(scope="function")
def user_function(users_public_client: UsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = users_public_client.create_user(request=request)
    return UserFixture(request=request, response=response)

@pytest.fixture(scope="function")
def users_private_client(auth_client) -> UsersClient:
    return get_private_users_client(auth=auth_client)