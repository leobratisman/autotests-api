import allure
from typing import Any

from jsonschema import validate
from jsonschema.validators import Draft202012Validator

from utils.logger import get_logger

logger = get_logger("JSON SCHEMA ASSERTIONS")

@allure.step("Validate JSON-schema")
def validate_json_schema(instance: Any, schema: dict) -> None:
    logger.info("Validate JSON-schema")

    validate(
        schema=schema,
        instance=instance,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )