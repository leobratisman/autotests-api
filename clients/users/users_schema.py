from pydantic import EmailStr, Field

from clients.base_schema import BaseSchema
from utils.fake_data_factory import faker


class CreateUserRequestSchema(BaseSchema):
    email: EmailStr = Field(default_factory=faker.email)
    password: str = Field(default_factory=faker.password)
    last_name: str = Field(alias="lastName", default_factory=faker.last_name)
    first_name: str = Field(alias="firstName", default_factory=faker.first_name)
    middle_name: str = Field(alias="middleName", default_factory=faker.first_name)

class UserSchema(BaseSchema):
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

class CreateUserResponseSchema(BaseSchema):
    user: UserSchema

class GetCurrentUserResponseSchema(CreateUserResponseSchema):
    pass

class GetUserResponseSchema(CreateUserResponseSchema):
    pass

class UpdateUserRequestSchema(BaseSchema):    
    email: EmailStr | None = Field(default_factory=faker.email)
    last_name: str | None = Field(alias="lastName", default_factory=faker.last_name)
    first_name: str | None = Field(alias="firstName", default_factory=faker.first_name)
    middle_name: str | None = Field(alias="middleName", default_factory=faker.middle_name)

class UpdateUserResponseSchema(CreateUserResponseSchema):
    pass