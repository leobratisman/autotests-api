from http import HTTPStatus
import pytest, allure

from clients.users.users_schema import (
    CreateUserRequestSchema,
    UpdateUserRequestSchema
)
from clients.users.users_client import UsersClient
from clients.errors_schema import InternalErrorResponseSchema

from utils.assertions.users import (
    assert_create_user_response,
    assert_get_current_user_response,
    assert_get_user_response,
    assert_update_user_response,
    assert_user_not_found_response
)
from utils.assertions.base import assert_status_code
from utils.fake_data_factory import faker

from tests.fixtures.users import UserFixture

from utils.allure.tags import AllureTag
from utils.allure.severity import Severity
from utils.allure.epics import AllureEpic
from utils.allure.features import AllureFeature
from utils.allure.suites import AllureParentSuite, AllureSubSuite, AllureSuite
from utils.allure.stories import AllureStory


@pytest.mark.regress
@pytest.mark.users
@pytest.mark.smoke
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION, AllureTag.SMOKE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@allure.severity(Severity.BLOCKER)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.USERS)
class TestUsers:
    @allure.title("Create user")
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @pytest.mark.parametrize("domain", ["yandex.ru", "gmail.com", "example.com"])
    def test_create_user(self, users_public_client: UsersClient, domain: str):
        request = CreateUserRequestSchema(email=faker.email(domain=domain))
        response = users_public_client.create_user(request=request)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(
            request=request,
            response=response.schema
        )

    @allure.title("Get current user")
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    def test_get_current_user(self, user_function, users_private_client: UsersClient):
        response = users_private_client.get_current_user()

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        assert_get_current_user_response(create_user_response=user_function.response.schema, response=response.schema)

    @allure.title("Get user")
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    def test_get_user(self, user_function: UserFixture, users_private_client: UsersClient):
        response = users_private_client.get_user(user_id=user_function.response.schema.user.id)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        assert_get_user_response(create_user_response=user_function.response.schema, response=response.schema)

    @allure.title("Update user")
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.UPDATE_ENTITY)
    def test_update_user(self, user_function: UserFixture, users_private_client: UsersClient):
        request = UpdateUserRequestSchema()
        response = users_private_client.update_user(user_id=user_function.response.schema.user.id, request=request)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        assert_update_user_response(request=request, response=response.schema)

    @allure.title("Delete user")
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureSubSuite.DELETE_ENTITY)
    def test_delete_user(self, users_private_client: UsersClient):
        request = CreateUserRequestSchema()
        create_user_response = users_private_client.create_user(request=request)

        response = users_private_client.delete_user(user_id=create_user_response.schema.user.id)
        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)

        response = users_private_client.get_user(user_id=create_user_response.schema.user.id)
        response_data = InternalErrorResponseSchema.model_validate_json(response.raw_response)
        assert_status_code(actual=response.status_code, expected=HTTPStatus.NOT_FOUND)
        assert_user_not_found_response(response_data)