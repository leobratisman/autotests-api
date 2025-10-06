from pydantic import Field, HttpUrl

from clients.base_schema import BaseSchema
from utils.fake_data_factory import faker


class FileSchema(BaseSchema):
    id: str
    filename: str
    directory: str
    url: HttpUrl

class CreateFileRequestSchema(BaseSchema):
    filename: str = Field(max_length=255, default_factory=faker.uuid4)
    directory: str = Field(max_length=1024, default="tests")
    upload_file: str = Field(default_factory=faker.file_path)

class CreateFileResponseSchema(BaseSchema):
    file: FileSchema

class GetFileResponseSchema(BaseSchema):
    file: FileSchema

