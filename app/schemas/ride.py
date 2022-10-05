import uuid
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.common.base import RWSchema
from app.schemas.geojson import PointGeometry


class Ride(RWSchema, BaseModel):
    id: uuid.UUID
    position: Optional[PointGeometry]


class RideCollection(RWSchema, BaseModel):
    rides: List[Ride]
