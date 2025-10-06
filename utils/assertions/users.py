import allure

from utils.assertions.base import assert_equal

from clients.users.users_schema import (
    CreateUserResponseSchema, 
    CreateUserRequestSchema,
    GetCurrentUserResponseSchema,
    GetUserResponseSchema,
    UpdateUserRequestSchema,
    UserSchema
)
from utils.assertions.errors import InternalErrorResponseSchema, assert_internal_error_response

from utils.logger import get_logger

logger = get_logger("USERS ASSERTIONS")


@allure.step("Check user")
def assert_user(actual: UserSchema, expected: UserSchema):
    logger.info("Check user")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")

@allure.step("Check create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    logger.info("Check create user response")

    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")

@allure.step("Check get current user response")
def assert_get_current_user_response(create_user_response: CreateUserResponseSchema, response: GetCurrentUserResponseSchema):
    logger.info("Check get current user response")

    assert_user(actual=response.user, expected=create_user_response.user)

@allure.step("Check get user response")
def assert_get_user_response(create_user_response: CreateUserResponseSchema, response: GetCurrentUserResponseSchema):
    logger.info("Check get user response")

    assert_user(actual=response.user, expected=create_user_response.user)

@allure.step("Check update user response")
def assert_update_user_response(request: UpdateUserRequestSchema, response: GetUserResponseSchema):
    logger.info("Check update user response")

    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")

@allure.step("Check user not found response")
def assert_user_not_found_response(actual: InternalErrorResponseSchema):
    logger.info("Check user not found response")

    expected = InternalErrorResponseSchema(details="User not found")
    assert_internal_error_response(actual, expected)