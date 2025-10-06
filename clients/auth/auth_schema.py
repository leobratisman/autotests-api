from pydantic import EmailStr, Field

from clients.base_schema import BaseSchema

from utils.fake_data_factory import faker


class LoginRequestSchema(BaseSchema, frozen=True):
    email: EmailStr | None = Field(default_factory=faker.email)
    password: str | None = Field(default_factory=faker.password)

class TokenSchema(BaseSchema):
    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")

class LoginResponseSchema(BaseSchema):
    token: TokenSchema

class RefreshRequestSchema(BaseSchema):
    refresh_token: str | None = Field(alias="refreshToken", default_factory=faker.uuid4)

class RefreshResponseSchema(BaseSchema):
    token: TokenSchema