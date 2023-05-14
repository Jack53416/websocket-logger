import uuid

from pydantic import BaseModel

from app.schemas.common.base import RWSchema
from app.schemas.geojson import FeatureCollection
from app.schemas.quay import Quay
from app.schemas.route import Route


class Tenant(RWSchema, BaseModel):
    name: str


class Vehicle(RWSchema, BaseModel):
    id: uuid.UUID


class Line(RWSchema, BaseModel):
    id: uuid.UUID
    name: str
    short_name: str | None
    number: str | None


class Trip(RWSchema, BaseModel):
    vehicle: Vehicle
    eta: int
    line: Line
    route: Route
    quays: list[Quay]
    tenant: Tenant


class TripCollection(RWSchema, BaseModel):
    __root__:  list[Trip]


class TripGeometryCollection(RWSchema, BaseModel):
    __root__:  dict[uuid.UUID, FeatureCollection]
