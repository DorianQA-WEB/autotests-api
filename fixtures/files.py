from clients.files.files_client import get_files_client, FilesClient
import pytest
from fixtures.users import UserFixture
from clients.files.file_schema import CreateFileRequestSchema, CreateFileResponseSchema
from pydantic import BaseModel


class FileFixture(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema


@pytest.fixture
def files_client(function_user: UserFixture) -> FilesClient:
    return get_files_client(function_user.authentication_user)


@pytest.fixture
def function_files(files_client: FilesClient) -> FileFixture:
    request = CreateFileRequestSchema(upload_file="./testdata/files/space.jpg")
    response = files_client.create_file(request)
    return FileFixture(request=request, response=response)
