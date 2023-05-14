import uuid
from typing import Optional

from pydantic import BaseModel

from app.schemas.common.base import RWSchema
from app.schemas.geojson import PointGeometry


class Ride(RWSchema, BaseModel):
    id: uuid.UUID
    position: Optional[PointGeometry]


class RideCollection(RWSchema, BaseModel):
    __root__: list[Ride]
