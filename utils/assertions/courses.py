from typing import List
import allure

from utils.assertions.base import assert_equal

from clients.courses.courses_schema import (
    UpdateCourseRequestSchema, 
    GetCourseResponseSchema,
    GetCoursesResponseSchema,
    CreateCourseResponseSchema,
    CreateCourseRequestSchema,
    CourseSchema
)
from clients.errors_schema import InternalErrorResponseSchema

from utils.assertions.files import assert_file
from utils.assertions.users import assert_user
from utils.assertions.errors import assert_internal_error_response

from utils.logger import get_logger

logger = get_logger("COURSES ASSERTIONS")


@allure.step("Check course")
def assert_course(actual: CourseSchema, expected: CourseSchema):
    logger.info("Check course")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")
    assert_user(actual=actual.created_by_user, expected=expected.created_by_user)
    assert_file(actual=actual.preview_file, expected=expected.preview_file)

@allure.step("Check create course response")
def assert_create_course_response(request: CreateCourseRequestSchema, response: GetCourseResponseSchema):
    logger.info("Check create course response")

    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")
    assert_equal(actual=response.course.created_by_user.id, expected=request.created_by_user_id, name="created_by_user_id")
    assert_equal(actual=response.course.preview_file.id, expected=request.preview_file_id, name="preview_file_id")

@allure.step("Check get course response")
def assert_get_course_response(create_course_response: CreateCourseResponseSchema, response: GetCourseResponseSchema):
    logger.info("Check get course response")

    assert_course(actual=response.course, expected=create_course_response.course)

@allure.step("Check get courses response")
def assert_get_courses_response(
    response: GetCoursesResponseSchema, 
    create_courses_response: List[CreateCourseResponseSchema]
):
    logger.info("Check get courses response")

    for index, course in enumerate(create_courses_response):
        assert_course(actual=response.courses[index], expected=course.course)

@allure.step("Check update course response")
def assert_update_course_response(request: UpdateCourseRequestSchema, response: GetCourseResponseSchema):
    logger.info("Check update course response")

    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Check course not found response")
def assert_course_not_found_response(actual: InternalErrorResponseSchema):
    logger.info("Check course not found response")

    expected = InternalErrorResponseSchema(details="Course not found")
    assert_internal_error_response(actual, expected)