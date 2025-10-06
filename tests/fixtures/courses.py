import pytest
from pydantic import BaseModel

from clients.deps import AuthClient, get_courses_client
from clients.courses.courses_client import CoursesClient

from clients.base_schema import ApiResponse
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema

from tests.fixtures.files import FileFixture
from tests.fixtures.users import UserFixture


class CourseFixture(BaseModel):
    request: CreateCourseRequestSchema
    response: ApiResponse[CreateCourseResponseSchema]


@pytest.fixture(scope="function")
def courses_client(auth_client: AuthClient) -> CoursesClient:
    return get_courses_client(auth=auth_client)

@pytest.fixture(scope="function")
def course_function(
    courses_client: CoursesClient,
    file_function: FileFixture,
    user_function: UserFixture
) -> CourseFixture:
    request = CreateCourseRequestSchema(
        preview_file_id=file_function.response.schema.file.id,
        created_by_user_id=user_function.response.schema.user.id
    )
    response = courses_client.create_course(request=request)

    return CourseFixture(
        request=request,
        response=response
    )
