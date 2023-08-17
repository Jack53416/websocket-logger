import uuid

from pydantic import BaseModel

from app.schemas.common.base import RWSchema
from app.schemas.geojson import PointGeometry


class VehicleEta(RWSchema, BaseModel):
    quay_id: uuid.UUID
    eta: int


class VehicleBase(BaseModel):
    id: uuid.UUID


class VehicleInDb(RWSchema, VehicleBase):
    pass


class Vehicle(VehicleInDb):
    position: PointGeometry
    eta: list[VehicleEta]
