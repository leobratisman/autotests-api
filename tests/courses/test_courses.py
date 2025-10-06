import pytest, http
import allure

from tests.fixtures.courses import CourseFixture
from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import (
    UpdateCourseRequestSchema, 
    CreateCourseRequestSchema,
    GetCoursesRequestSchema
)
from clients.errors_schema import InternalErrorResponseSchema

from utils.assertions.base import assert_status_code
from utils.assertions.courses import (
    assert_update_course_response,
    assert_get_course_response,
    assert_get_courses_response,
    assert_create_course_response,
    assert_course_not_found_response
)

from tests.fixtures.users import UserFixture
from tests.fixtures.files import FileFixture

from utils.allure.tags import AllureTag
from utils.allure.severity import Severity
from utils.allure.epics import AllureEpic
from utils.allure.features import AllureFeature
from utils.allure.suites import AllureParentSuite, AllureSubSuite, AllureSuite
from utils.allure.stories import AllureStory



@pytest.mark.regress
@pytest.mark.courses
@pytest.mark.smoke
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION, AllureTag.SMOKE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.severity(Severity.CRITICAL)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.COURSES)
class TestCourses:
    @allure.title("Create course")
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    def test_create_course(self, courses_client: CoursesClient, user_function: UserFixture, file_function: FileFixture):
        request = CreateCourseRequestSchema(
            created_by_user_id=user_function.response.schema.user.id,
            preview_file_id=file_function.response.schema.file.id
        )
        response = courses_client.create_course(request=request)
        assert_status_code(response.status_code, http.HTTPStatus.OK)

        response = courses_client.get_course(course_id=response.schema.course.id)
        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_create_course_response(request, response.schema)

    @allure.title("Get course")
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    def test_get_course(self, course_function: CourseFixture, courses_client: CoursesClient):
        response = courses_client.get_course(course_id=course_function.response.schema.course.id)

        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_get_course_response(course_function.response.schema, response.schema)

    @allure.title("Get courses")
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    def test_get_courses(self, courses_client: CoursesClient, user_function: UserFixture, file_function: FileFixture):
        requests = [
            CreateCourseRequestSchema(
                created_by_user_id=user_function.response.schema.user.id,
                preview_file_id=file_function.response.schema.file.id
            ) for _ in range(3)
        ]
        create_course_responses = []
        for request in requests:
            response = courses_client.create_course(request=request)
            assert_status_code(response.status_code, http.HTTPStatus.OK)
            create_course_responses.append(response.schema)
        
        response = courses_client.get_courses(
            request=GetCoursesRequestSchema(user_id=user_function.response.schema.user.id)
        )

        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_get_courses_response(response.schema, create_course_responses)

    @allure.title("Update course")
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.UPDATE_ENTITY)
    def test_update_course(self, course_function: CourseFixture, courses_client: CoursesClient):
        request = UpdateCourseRequestSchema()
        response = courses_client.update_course(
            course_id=course_function.response.schema.course.id,
            request=request
        )
        assert_status_code(response.status_code, http.HTTPStatus.OK)

        response = courses_client.get_course(course_id=course_function.response.schema.course.id)

        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_update_course_response(request, response.schema)

    @allure.title("Delete course")
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureSubSuite.DELETE_ENTITY)
    def test_delete_course(self, course_function: CourseFixture, courses_client: CoursesClient):
        response = courses_client.delete_course(course_id=course_function.response.schema.course.id)
        assert_status_code(response.status_code, http.HTTPStatus.OK)

        response = courses_client.get_course(course_id=course_function.response.schema.course.id)
        assert_status_code(response.status_code, http.HTTPStatus.NOT_FOUND)

        response_data = InternalErrorResponseSchema.model_validate_json(response.raw_response)
        assert_course_not_found_response(actual=response_data)