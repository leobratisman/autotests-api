import pytest, http
import allure

from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    UpdateExerciseRequestSchema,
    GetExercisesRequestSchema
)
from clients.exercises.exercises_client import ExercisesClient
from clients.errors_schema import InternalErrorResponseSchema

from utils.assertions.base import assert_status_code
from utils.assertions.exercises import (
    assert_create_exercise_response,
    assert_get_exercise_response,
    assert_get_exercises_response,
    assert_update_exercise_response,
    assert_exercise_not_found_response
)

from tests.fixtures.courses import CourseFixture
from tests.fixtures.exercises import ExerciseFixture

from utils.allure.tags import AllureTag
from utils.allure.severity import Severity
from utils.allure.epics import AllureEpic
from utils.allure.features import AllureFeature
from utils.allure.suites import AllureParentSuite, AllureSubSuite, AllureSuite
from utils.allure.stories import AllureStory



@pytest.mark.regress
@pytest.mark.exercises
@pytest.mark.smoke
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION, AllureTag.SMOKE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@allure.severity(Severity.CRITICAL)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.EXERCISES)
class TestExercises:
    @allure.title("Create exercise")
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    def test_create_exercises(self, course_function: CourseFixture, exercises_client: ExercisesClient):
        request = CreateExerciseRequestSchema(
            course_id=course_function.response.schema.course.id,
        )
        response = exercises_client.create_exercise(request=request)
        assert_status_code(response.status_code, http.HTTPStatus.OK)

        response = exercises_client.get_exercise(exercises_id=response.schema.exercise.id)
        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_create_exercise_response(request, response.schema)

    @allure.title("Get exercise")
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    def test_get_exercise(self, exercise_function: ExerciseFixture, exercises_client: ExercisesClient):
        response = exercises_client.get_exercise(exercises_id=exercise_function.response.schema.exercise.id)

        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_get_exercise_response(exercise_function.response.schema, response.schema)

    @allure.title("Get exercises")
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    def test_get_exercises(self, exercises_client: ExercisesClient, course_function: CourseFixture):
        requests = [
            CreateExerciseRequestSchema(
                course_id=course_function.response.schema.course.id,
            ) for _ in range(3)
        ]
        create_exercise_responses = []
        for request in requests:
            response = exercises_client.create_exercise(request=request)
            assert_status_code(response.status_code, http.HTTPStatus.OK)
            create_exercise_responses.append(response.schema)
        
        response = exercises_client.get_exercises(
            request=GetExercisesRequestSchema(course_id=course_function.response.schema.course.id)
        )

        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_get_exercises_response(response.schema, create_exercise_responses)

    @allure.title("Update exercise")
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.UPDATE_ENTITY)
    def test_update_exercise(self, exercise_function: ExerciseFixture, exercises_client: ExercisesClient):
        request = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise(
            exercises_id=exercise_function.response.schema.exercise.id,
            request=request
        )
        assert_status_code(response.status_code, http.HTTPStatus.OK)

        response = exercises_client.get_exercise(exercises_id=exercise_function.response.schema.exercise.id)

        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_update_exercise_response(request, response.schema)

    @allure.title("Delete exercise")
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureSubSuite.DELETE_ENTITY)
    def test_delete_exercise(self, exercise_function: ExerciseFixture, exercises_client: ExercisesClient):
        response = exercises_client.delete_exercise(exercises_id=exercise_function.response.schema.exercise.id)
        assert_status_code(response.status_code, http.HTTPStatus.OK)

        response = exercises_client.get_exercise(exercises_id=exercise_function.response.schema.exercise.id)
        assert_status_code(response.status_code, http.HTTPStatus.NOT_FOUND)

        response_data = InternalErrorResponseSchema.model_validate_json(response.raw_response)
        assert_exercise_not_found_response(actual=response_data)
