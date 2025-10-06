import pytest
from pydantic import BaseModel

from clients.deps import AuthClient, get_files_client
from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.base_schema import ApiResponse

from config import settings


class FileFixture(BaseModel):
    request: CreateFileRequestSchema
    response: ApiResponse[CreateFileResponseSchema]


@pytest.fixture(scope="function")
def files_client(auth_client: AuthClient) -> FilesClient:
    return get_files_client(auth=auth_client)

@pytest.fixture(scope="function")
def file_function(files_client: FilesClient) -> FileFixture:
    request = CreateFileRequestSchema(upload_file=settings.file_path(filename="image.png"))
    response = files_client.create_file(request=request)

    return FileFixture(
        request=request,
        response=response
    )