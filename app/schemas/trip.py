import uuid
from enum import Enum
from typing import List

from pydantic import BaseModel

from app.schemas.common.base import RWSchema
from app.schemas.geojson import FeatureCollection
from app.schemas.quay import Quay
from app.schemas.route import Route


class TripPartType(str, Enum):
    VEHICLE = "VEHICLE"


class Tenant(RWSchema, BaseModel):
    name: str


class Line(RWSchema, BaseModel):
    id: uuid.UUID
    name: str
    short_name: str | None
    number: str | None


class TripPart(RWSchema, BaseModel):
    line: Line
    route: Route
    quays: List[Quay]
    route_geometry: FeatureCollection
    trip_part_type: TripPartType = TripPartType.VEHICLE


class Trip(RWSchema, BaseModel):
    tenant: Tenant
    trip_parts: List[TripPart]
    starts_in: int


class TripCollection(BaseModel):
    trips: List[Trip]
