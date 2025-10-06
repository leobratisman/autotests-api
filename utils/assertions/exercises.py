from typing import List
import allure

from utils.assertions.base import assert_equal

from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    GetExercisesResponseSchema,
    ExerciseSchema,
    UpdateExerciseResponseSchema
)
from clients.errors_schema import InternalErrorResponseSchema

from utils.assertions.errors import assert_internal_error_response
from utils.logger import get_logger

logger = get_logger("EXERCISES ASSERTIONS")


@allure.step("Check exercise")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    logger.info("Check exercise")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

@allure.step("Check create exercise response")
def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: GetExerciseResponseSchema):
    logger.info("Check create exercise response")

    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Check get exercise response")
def assert_get_exercise_response(create_exercise_response: CreateExerciseResponseSchema, response: GetExerciseResponseSchema):
    logger.info("Check get exercise response")

    assert_exercise(actual=response.exercise, expected=create_exercise_response.exercise)

@allure.step("Check get exercises response")
def assert_get_exercises_response(
    response: GetExercisesResponseSchema, 
    create_exercises_response: List[CreateExerciseResponseSchema]
):
    logger.info("Check get exercises response")

    for index, exercise in enumerate(create_exercises_response):
        assert_exercise(actual=response.exercises[index], expected=exercise.exercise)

@allure.step("Check update exercise response")
def assert_update_exercise_response(request: UpdateExerciseResponseSchema, response: GetExerciseResponseSchema):
    logger.info("Check update exercise response")

    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Check exercise not found response")
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    logger.info("Check exercise not found response")

    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual, expected)