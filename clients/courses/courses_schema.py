from pydantic import Field
from typing import List

from clients.base_schema import BaseSchema
from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema

from utils.fake_data_factory import faker


class CourseSchema(BaseSchema):
    id: str
    title: str = Field(min_length=1, max_length=250)
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    description: str = Field(min_length=1)
    preview_file: FileSchema = Field(alias="previewFile")
    estimated_time: str | None = Field(alias="estimatedTime")
    created_by_user: UserSchema = Field(alias="createdByUser")

class CreateCourseRequestSchema(BaseSchema):
    title: str = Field(min_length=1, max_length=250, default_factory=faker.title)
    max_score: int | None = Field(alias="maxScore", default_factory=faker.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=faker.min_score)
    description: str = Field(min_length=1, default_factory=faker.description)
    preview_file_id: str = Field(alias="previewFileId", default_factory=faker.uuid4)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=faker.estimated_time)
    created_by_user_id: str = Field(alias="createdByUserId", default_factory=faker.uuid4)

class CreateCourseResponseSchema(BaseSchema):
    course: CourseSchema
    
class GetCourseResponseSchema(BaseSchema):
    course: CourseSchema

class GetCoursesRequestSchema(BaseSchema):
    user_id: str = Field(alias="userId", default_factory=faker.uuid4)

class GetCoursesResponseSchema(BaseSchema):
    courses: List[CourseSchema]

class UpdateCourseRequestSchema(BaseSchema):
    title: str | None = Field(max_length=250, default_factory=faker.title)
    max_score: int | None = Field(alias="maxScore", default_factory=faker.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=faker.min_score)
    description: str | None = Field(default_factory=faker.description)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=faker.estimated_time)

class UpdateCourseResponseSchema(BaseSchema):
    course: CourseSchema
