import pytest
from pydantic import BaseModel

from clients.deps import AuthClient, get_exercises_client
from clients.base_schema import ApiResponse
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema

from tests.fixtures.courses import CourseFixture


class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: ApiResponse[CreateExerciseResponseSchema]


@pytest.fixture(scope="function")
def exercises_client(auth_client: AuthClient) -> ExercisesClient:
    return get_exercises_client(auth=auth_client)

@pytest.fixture(scope="function")
def exercise_function(
    exercises_client: ExercisesClient,
    course_function: CourseFixture
) -> ExerciseFixture:
    request = CreateExerciseRequestSchema(course_id=course_function.response.schema.course.id)
    response = exercises_client.create_exercise(request=request)

    return ExerciseFixture(
        request=request,
        response=response
    )