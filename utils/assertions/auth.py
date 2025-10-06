import allure

from utils.assertions.base import assert_equal, assert_is_true
from clients.auth.auth_schema import LoginResponseSchema, RefreshResponseSchema

from utils.logger import get_logger

logger = get_logger("AUTH ASSERTIONS")


@allure.step("Check login response")
def assert_login_response(response: LoginResponseSchema):
    logger.info("Check login response")

    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")


@allure.step("Check refresh response")
def assert_refresh_response(response: RefreshResponseSchema):
    logger.info("Check refresh response")

    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")