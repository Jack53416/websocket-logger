from typing import List

from pydantic import BaseModel

from app.schemas.common.base import RWSchema


class City(RWSchema, BaseModel):
    name: str
    country: str
    country_code: str
    bbox: List[float]


class CitiesCollection(BaseModel):
    __root__: list[City]
