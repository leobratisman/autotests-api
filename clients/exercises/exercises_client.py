import allure

from clients.base_client import BaseHTTPClient
from clients.auth.auth_client import auth

from utils.mapper import Mapper
from utils.assertions.schema import validate_json_schema

from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExercisesResponseSchema,
    GetExercisesRequestSchema,
    GetExerciseResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema
)
from clients.base_schema import ApiResponse


class ExercisesClient(BaseHTTPClient):
    def __init__(self, client, auth = None):
        super().__init__(client, auth)
        self.__endpoint = "/exercises"

    @auth
    @allure.step("Create exercise")
    def create_exercise(self, request: CreateExerciseRequestSchema, **kwargs) -> ApiResponse[CreateExerciseResponseSchema]:
        try:
            response = self._post(endpoint=self.__endpoint, json=Mapper.schema_to_dict(request), **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), CreateExerciseResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, CreateExerciseResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to create exercise: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Get exercises by course")
    def get_exercises(self, request: GetExercisesRequestSchema, **kwargs) -> ApiResponse[GetExercisesResponseSchema]:
        try:
            response = self._get(endpoint=self.__endpoint, params=Mapper.schema_to_dict(request), **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), GetExercisesResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, GetExercisesResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to get exercises: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Get exercise by ID")
    def get_exercise(self, exercises_id: str, **kwargs) -> ApiResponse[GetExerciseResponseSchema]:
        endpoint = f"{self.__endpoint}/{exercises_id}"
        try:
            response = self._get(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            validate_json_schema(response.json(), GetExerciseResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, GetExerciseResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to get exercise: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Update exercise by ID")
    def update_exercise(
        self, 
        exercises_id: str, 
        request: UpdateExerciseRequestSchema, 
        **kwargs
    ) -> ApiResponse[UpdateExerciseResponseSchema]:
        endpoint = f"{self.__endpoint}/{exercises_id}"
        try:
            response = self._patch(
                endpoint=endpoint, 
                json=Mapper.schema_to_dict(request, exclude_none=True), 
                **kwargs
            )
            response.raise_for_status()
            validate_json_schema(response.json(), UpdateExerciseResponseSchema.model_json_schema())

            return ApiResponse(
                schema=Mapper.json_to_schema(response.text, UpdateExerciseResponseSchema),
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to update exercise: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )

    @auth
    @allure.step("Delete exercise by ID")
    def delete_exercise(self, exercises_id: str, **kwargs) -> ApiResponse:
        endpoint = f"{self.__endpoint}/{exercises_id}"
        try:
            response = self._delete(endpoint=endpoint, **kwargs)
            response.raise_for_status()
            return ApiResponse(
                status_code=response.status_code
            )
        except Exception as e:
            self.logger.error(f"Failed to delete exercise: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )