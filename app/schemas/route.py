import uuid

from pydantic import BaseModel

from app.schemas.common.base import RWSchema


class Route(RWSchema, BaseModel):
    id: uuid.UUID
