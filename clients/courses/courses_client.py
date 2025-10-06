import allure

from clients.base_client import BaseHTTPClient
from clients.auth.auth_client import auth

from utils.mapper import Mapper
from utils.assertions.schema import validate_json_schema

from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCourseResponseSchema,
    GetCoursesRequestSchema,
    GetCoursesResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema
)
from clients.base_schema import ApiResponse



class CoursesClient(BaseHTTPClient):
    def __init__(self, client, auth = None):
        super().__init__(client, auth)
        self.__endpoint = "/courses"

    @auth
    @allure.step("Create course")
    def create_course(self, request: CreateCourseRequestSchema, **kwargs) -> ApiResponse[CreateCourseResponseSchema]:
        try:
            response = self._post(endpoint=self.__endpoint, json=Mapper.schema_to_dict(request), **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), CreateCourseResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, CreateCourseResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to create course: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Get courses by user")
    def get_courses(self, request: GetCoursesRequestSchema, **kwargs) -> ApiResponse[GetCoursesResponseSchema]:
        try:
            response = self._get(endpoint=self.__endpoint, params=Mapper.schema_to_dict(request), **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), GetCoursesResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, GetCoursesResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to get courses: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Get course by ID")
    def get_course(self, course_id: str, **kwargs) -> ApiResponse[GetCourseResponseSchema]:
        endpoint = f"{self.__endpoint}/{course_id}"
        try:
            response = self._get(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), GetCourseResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, GetCourseResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to get course: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Update course by ID")
    def update_course(
        self, 
        course_id: str, 
        request: UpdateCourseRequestSchema, 
        **kwargs
    ) -> ApiResponse[UpdateCourseResponseSchema]:
        endpoint = f"{self.__endpoint}/{course_id}"
        try:
            response = self._patch(
                endpoint=endpoint, 
                json=Mapper.schema_to_dict(request, exclude_none=True), 
                **kwargs
            )
            response.raise_for_status()
            validate_json_schema(response.json(), UpdateCourseResponseSchema.model_json_schema())
            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, UpdateCourseResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to update course: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Delete course by ID")
    def delete_course(self, course_id: str, **kwargs) -> ApiResponse:
        endpoint = f"{self.__endpoint}/{course_id}"
        try:
            response = self._delete(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            return ApiResponse(
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to delete course: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )