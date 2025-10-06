import allure

from clients.errors_schema import ValidationErrorSchema, ValidationErrorResponseSchema, InternalErrorResponseSchema
from utils.assertions.base import assert_equal, assert_length

from utils.logger import get_logger

logger = get_logger("ERRORS ASSERTIONS")


@allure.step("Check validation error schema")
def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    logger.info("Check validation error schema")

    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.location, expected.location, "location")

@allure.step("Check validation error from response")
def assert_validation_error_response(
    actual: ValidationErrorResponseSchema,
    expected: ValidationErrorResponseSchema
):
    logger.info("Check validation error from response")

    assert_length(actual.details, expected.details, "details")

    for index, detail in enumerate(expected.details):
        assert_validation_error(actual.details[index], detail)

@allure.step("Check internal error from response")
def assert_internal_error_response(
    actual: InternalErrorResponseSchema,
    expected: InternalErrorResponseSchema
):
    logger.info("Check internal error from response")

    assert_equal(actual.details, expected.details, "details")