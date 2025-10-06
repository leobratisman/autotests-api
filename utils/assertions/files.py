import httpx, http
import allure

from utils.assertions.base import assert_equal, assert_status_code

from clients.files.files_schema import (
    CreateFileResponseSchema, 
    CreateFileRequestSchema,
    GetFileResponseSchema,
    FileSchema
)
from clients.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema, InternalErrorResponseSchema
from utils.assertions.base import assert_equal
from utils.assertions.errors import assert_validation_error_response, assert_internal_error_response

from utils.logger import get_logger

logger = get_logger("FILES ASSERTIONS")


@allure.step("Check file")
def assert_file(actual: FileSchema, expected: FileSchema):
    logger.info("Check file")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.url, expected.url, "url")
    assert_equal(actual.filename, expected.filename, "filename")
    assert_equal(actual.directory, expected.directory, "directory")

@allure.step("Check that file is accessible")
def assert_file_is_accessible(url: str):
    logger.info("Check that file is accessible")

    response = httpx.get(url)
    assert_status_code(response.status_code, http.HTTPStatus.OK)

@allure.step("Check create file response")
def assert_create_file_response(request: CreateFileRequestSchema, response: CreateFileResponseSchema):
    logger.info("Check create file response")

    expected_url = f"http://localhost:8000/static/{request.directory}/{request.filename}"

    assert_equal(str(response.url), expected_url, "url")
    assert_equal(response.filename, request.filename, "filename")
    assert_equal(response.directory, request.directory, "directory")

    assert_file_is_accessible(expected_url)

@allure.step("Check get file response")
def assert_get_file_response(create_file_response: CreateFileResponseSchema, response: GetFileResponseSchema):
    logger.info("Check get file response")

    assert_file(actual=response.file, expected=create_file_response.file)

@allure.step("Check create file with empty filename response")
def assert_create_file_with_empty_filename_response(actual: ValidationErrorResponseSchema):
    logger.info("Check create file with empty filename response")

    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", "filename"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check create file with empty directory response")
def assert_create_file_with_empty_directory_response(actual: ValidationErrorResponseSchema):
    logger.info("Check create file with empty directory response")

    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", "directory"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check file not found response")
def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    logger.info("Check file not found response")

    expected = InternalErrorResponseSchema(details="File not found")
    assert_internal_error_response(actual, expected)

@allure.step("Check get file with incorrect ID response")
def assert_get_file_with_incorrect_file_id(actual: ValidationErrorResponseSchema):
    logger.info("Check get file with incorrect ID response")

    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect_file_id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
                },
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["path", "file_id"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)