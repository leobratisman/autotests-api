import pytest, http
import allure

from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema
from clients.errors_schema import ValidationErrorResponseSchema, InternalErrorResponseSchema

from utils.assertions.files import assert_create_file_response, assert_get_file_response
from utils.assertions.base import assert_status_code

from tests.fixtures.files import FileFixture
from utils.assertions.files import (
    assert_create_file_with_empty_filename_response, 
    assert_create_file_with_empty_directory_response,
    assert_file_not_found_response,
    assert_get_file_with_incorrect_file_id
)

from config import settings

from utils.allure.tags import AllureTag
from utils.allure.severity import Severity
from utils.allure.epics import AllureEpic
from utils.allure.features import AllureFeature
from utils.allure.suites import AllureParentSuite, AllureSubSuite, AllureSuite
from utils.allure.stories import AllureStory


@pytest.mark.regress
@pytest.mark.files
@allure.tag(AllureTag.FILES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@allure.severity(Severity.CRITICAL)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.FILES)
class TestFiles:
    @allure.title("Create file")
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    def test_create_file(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            upload_file=settings.file_path(filename="image.png")
        )
        response = files_client.create_file(request=request)

        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_create_file_response(request, response.schema.file)

    @allure.title("Get file")
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    def test_get_file(self, files_client: FilesClient, file_function: FileFixture):
        response = files_client.get_file(file_id=file_function.response.schema.file.id)

        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_get_file_response(file_function.response.schema, response.schema)

    @allure.title("Get files")
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    def test_delete_file(self, files_client: FilesClient, file_function: FileFixture):
        response = files_client.delete_file(file_id=file_function.response.schema.file.id)
        assert_status_code(response.status_code, http.HTTPStatus.OK)

        response = files_client.get_file(file_id=file_function.response.schema.file.id)
        assert_status_code(response.status_code, http.HTTPStatus.NOT_FOUND)

        response_data = InternalErrorResponseSchema.model_validate_json(response.raw_response)
        assert_file_not_found_response(actual=response_data)


@pytest.mark.regress
@pytest.mark.files
@pytest.mark.negative
@allure.tag(AllureTag.FILES, AllureTag.REGRESSION, AllureTag.NEGATIVE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@allure.severity(Severity.NORMAL)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.FILES)
class TestFilesNegative:
    @allure.title("Create file with empty filename")
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.VALIDATE_ENTITY)
    def test_create_file_with_empty_filename(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            filename="",
            upload_file=settings.file_path(filename="image.png")
        )
        response = files_client.create_file(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.raw_response)
        
        assert_status_code(response.status_code, http.HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_empty_filename_response(response_data)
        
    @allure.title("Create file with empty directory")
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.VALIDATE_ENTITY)
    def test_create_file_with_empty_directory(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            directory="",
            upload_file=settings.file_path(filename="image.png")
        )
        response = files_client.create_file(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.raw_response)
        
        assert_status_code(response.status_code, http.HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_empty_directory_response(response_data)

    @allure.title("Get file with incorrect file id")
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.VALIDATE_ENTITY)
    def test_get_file_with_incorrect_file_id(self, files_client: FilesClient, file_function: FileFixture):
        response = files_client.get_file(file_id="incorrect_file_id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.raw_response)
        
        assert_status_code(response.status_code, http.HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_file_with_incorrect_file_id(response_data)