from http import HTTPStatus
import pytest
import allure

from clients.deps import (
    get_auth_client
)
from utils.assertions.base import assert_status_code
from utils.assertions.auth import assert_login_response, assert_refresh_response

from clients.auth.auth_schema import LoginRequestSchema
from utils.allure.tags import AllureTag
from utils.allure.severity import Severity
from utils.allure.epics import AllureEpic
from utils.allure.features import AllureFeature
from utils.allure.suites import AllureParentSuite, AllureSubSuite, AllureSuite
from utils.allure.stories import AllureStory


@pytest.mark.regress
@pytest.mark.auth
@pytest.mark.smoke
@allure.tag(AllureTag.AUTH, AllureTag.REGRESSION, AllureTag.SMOKE)
@allure.severity(Severity.BLOCKER)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTH)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.AUTH)
class TestAuth:
    @allure.title("Login user with valid credentials")
    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureSubSuite.LOGIN)
    def test_login(self, user_function):
        request = LoginRequestSchema(
            email=user_function.email,
            password=user_function.password
        )
        client = get_auth_client(creds=request)

        assert_status_code(client.response.status_code, HTTPStatus.OK)
        assert_login_response(client.response.schema)

    
    @allure.title("Refresh user's tokens")
    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureSubSuite.LOGIN)
    def test_refresh(self, user_function):
        request = LoginRequestSchema(
            email=user_function.email,
            password=user_function.password
        )
        auth_client = get_auth_client(creds=request)
        response = auth_client.client.refresh()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_refresh_response(response.schema)
