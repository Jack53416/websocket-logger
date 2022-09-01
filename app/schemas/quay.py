import uuid
from typing import List

from pydantic import BaseModel

from app.schemas.common.base import RWSchema


class Quay(RWSchema, BaseModel):
    id: uuid.UUID
    name: str


class PlacesCollection(RWSchema, BaseModel):
    quays: List[Quay]
