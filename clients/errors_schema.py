from typing import Any

from pydantic import Field, ConfigDict
from clients.base_schema import BaseSchema


class ValidationErrorSchema(BaseSchema):
    type: str
    input: Any
    context: dict[str, Any] = Field(alias="ctx")
    message: str = Field(alias="msg")
    location: list[str] = Field(alias="loc")


class ValidationErrorResponseSchema(BaseSchema):
    details: list[ValidationErrorSchema] = Field(alias="detail")


class InternalErrorResponseSchema(BaseSchema):
    details: str = Field(alias="detail")
