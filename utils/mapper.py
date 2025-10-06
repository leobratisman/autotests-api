from clients.base_schema import BaseSchema

class Mapper:
    @classmethod
    def dict_to_schema(cls, data: dict, schema: BaseSchema, **kwargs) -> BaseSchema:
        return schema.model_validate(data, **kwargs)
    
    @classmethod
    def json_to_schema(cls, json: str, schema: BaseSchema, **kwargs) -> BaseSchema:
        return schema.model_validate_json(json, **kwargs)

    @classmethod 
    def schema_to_dict(cls, schema: BaseSchema, exclude_none: bool = False, **kwargs) -> dict:
        return schema.model_dump(exclude_none=exclude_none, **kwargs)
    
    @classmethod 
    def schema_to_json(cls, schema: BaseSchema, exclude_none: bool = False, **kwargs) -> str:
        return schema.model_dump_json(exclude_none=exclude_none, **kwargs)