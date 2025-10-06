from clients.deps import (
    get_public_users_client,
    get_auth_client,
    get_private_users_client,
    get_files_client,
    get_courses_client,
    get_exercises_client
)

from clients.auth.auth_schema import LoginRequestSchema
from clients.users.users_schema import (
    CreateUserRequestSchema, 
    CreateUserResponseSchema, 
    UpdateUserRequestSchema
)
from clients.files.files_schema import (
    CreateFileRequestSchema
)
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    GetCoursesRequestSchema
)
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    GetExercisesRequestSchema,
    UpdateExerciseRequestSchema
)

def main():
    users_client = get_public_users_client()

    create_user_request = CreateUserRequestSchema()

    create_user_response: CreateUserResponseSchema = users_client.create_user(request=create_user_request)
    print(create_user_response)

    auth_client = get_auth_client(creds=LoginRequestSchema(
        email=create_user_request.email,
        password=create_user_request.password
    ))

    users_client = get_private_users_client(auth=auth_client)

    user = users_client.get_user(user_id=create_user_response.user.id)
    print(user)

    update_user_request = UpdateUserRequestSchema()

    updated_user = users_client.update_user(user_id=create_user_response.user.id, request=update_user_request)
    print(updated_user)

    files_client = get_files_client(auth=auth_client)

    create_file_request = CreateFileRequestSchema(
        upload_file="./static/image.png"
    )

    create_file_request2 = CreateFileRequestSchema(
        upload_file="./static/image.png"
    )

    create_file_response = files_client.create_file(request=create_file_request)
    file = files_client.get_file(file_id=create_file_response.file.id)

    courses_client = get_courses_client(auth=auth_client)
    ex_client = get_exercises_client(auth=auth_client)

    create_course_request1 = CreateCourseRequestSchema(
        preview_file_id=file.file.id,
        created_by_user_id=user.user.id
    )

    create_course_response1 = courses_client.create_course(request=create_course_request1)
    get_course_response = courses_client.get_course(course_id=create_course_response1.course.id)
    
    get_courses_request = GetCoursesRequestSchema(user_id=user.user.id)

    create_ex_request = CreateExerciseRequestSchema(courseId=get_course_response.course.id,)

    create_ex_response = ex_client.create_exercise(request=create_ex_request)
    print(create_ex_response)

    get_exs_request = GetExercisesRequestSchema(course_id=get_course_response.course.id)

    get_exs_response = ex_client.get_exercises(request=get_exs_request)
    print(get_exs_response)

    get_ex_response = ex_client.get_exercise(exercises_id=create_ex_response.exercise.id)
    print(get_ex_response)

    response = courses_client.delete_course(course_id=create_course_response1.course.id)
    print(response.status_code)
    get_courses_response = courses_client.get_courses(request=get_courses_request)
    print(get_courses_response)
    
    response = users_client.delete_user(user_id=create_user_response.user.id)
    print(response.status_code)


if __name__ == "__main__":
    main()