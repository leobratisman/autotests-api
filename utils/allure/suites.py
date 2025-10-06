from enum import Enum


class AllureParentSuite(str, Enum):
    LMS = "LMS service"
    STUDENT = "Student service"
    ADMINISTRATION = "Administration service"

class AllureSuite(str, Enum):
    USERS = "Users"
    FILES = "Files"
    COURSES = "Courses"
    EXERCISES = "Exercises"
    AUTH = "Authentication"

class AllureSubSuite(str, Enum):
    LOGIN = "Login"

    GET_ENTITY = "Get entity"
    GET_ENTITIES = "Get entities"
    CREATE_ENTITY = "Create entity"
    UPDATE_ENTITY = "Update entity"
    DELETE_ENTITY = "Delete entity"
    VALIDATE_ENTITY = "Validate entity"


