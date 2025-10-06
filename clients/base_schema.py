from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True
    )

T = TypeVar("T", bound=BaseSchema)

class ApiResponse(BaseModel, Generic[T], ):
    schema: T | None = None
    status_code: int
    error: str | None = None
    raw_response: str | None = None

    def __repr__(self):
        return f"<ApiResponse(status_code={self.status_code}, schema={self.schema!r}, error={self.error!r}, raw_response={self.raw_response!r})>"
