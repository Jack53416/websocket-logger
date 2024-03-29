import uuid

from pydantic import BaseModel

from app.schemas.common.base import RWSchema
from app.schemas.quay import Quay


class Terminal(RWSchema, BaseModel):
    name: str
    code: str


class RouteBase(RWSchema, BaseModel):
    id: uuid.UUID


class TripRoute(RouteBase):
    start_terminal: Terminal
    end_terminal: Terminal


class Route(RouteBase):
    quays: list[Quay]
