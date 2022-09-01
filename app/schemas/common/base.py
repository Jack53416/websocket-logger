from datetime import datetime

from pydantic import BaseModel

from app.utils import to_camel_case, convert_datetime_to_real_world


class AliasedSchema(BaseModel):
    class Config(object):
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        json_encoders = {datetime: convert_datetime_to_real_world}


class RWSchema(AliasedSchema):
    class Config(object):
        orm_mode = True
