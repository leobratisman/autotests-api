from pydantic import Field
from typing import List

from clients.base_schema import BaseSchema

from utils.fake_data_factory import faker


class ExerciseSchema(BaseSchema):
    id: str
    title: str = Field(min_length=1, max_length=250)
    course_id: str = Field(alias="courseId")
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str = Field(min_length=1)
    estimated_time: str | None = Field(alias="estimatedTime")

class CreateExerciseRequestSchema(BaseSchema):
    title: str = Field(min_length=1, max_length=250, default_factory=faker.title)
    course_id: str = Field(alias="courseId", default_factory=faker.uuid4)
    max_score: int | None = Field(alias="maxScore", default_factory=faker.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=faker.min_score)
    order_index: int = Field(alias="orderIndex", default_factory=faker.integer)
    description: str = Field(min_length=1, default_factory=faker.description)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=faker.estimated_time)

class CreateExerciseResponseSchema(BaseSchema):
    exercise: ExerciseSchema

class GetExerciseResponseSchema(BaseSchema):
    exercise: ExerciseSchema

class GetExercisesRequestSchema(BaseSchema):
    course_id: str = Field(alias="courseId", default_factory=faker.uuid4)

class GetExercisesResponseSchema(BaseSchema):
    exercises: List[ExerciseSchema]

class UpdateExerciseRequestSchema(BaseSchema):
    title: str | None = Field(max_length=250, default_factory=faker.title)
    max_score: int | None = Field(alias="maxScore", default_factory=faker.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=faker.min_score)
    order_index: int | None = Field(alias="orderIndex", default_factory=faker.integer)
    description: str | None = Field(default_factory=faker.description)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=faker.estimated_time)

class UpdateExerciseResponseSchema(BaseSchema):
    exercise: ExerciseSchema
