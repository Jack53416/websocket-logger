import uuid

from pydantic import BaseModel

from app.schemas.common.base import RWSchema
from app.schemas.geojson import FeatureCollection
from app.schemas.quay import Quay
from app.schemas.route import TripRoute
from app.schemas.vehicle import VehicleInDb


class Tenant(RWSchema, BaseModel):
    name: str


class Line(RWSchema, BaseModel):
    id: uuid.UUID
    name: str
    short_name: str | None
    number: str | None


class Trip(RWSchema, BaseModel):
    vehicle: VehicleInDb
    eta: int
    line: Line
    route: TripRoute
    quays: list[Quay]
    tenant: Tenant


class TripCollection(RWSchema, BaseModel):
    __root__: list[Trip]


class TripGeometryCollection(RWSchema, BaseModel):
    __root__: dict[uuid.UUID, FeatureCollection]
