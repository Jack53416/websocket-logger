import uuid

from pydantic import BaseModel

from app.schemas.common.base import RWSchema


class Terminal(RWSchema, BaseModel):
    name: str
    code: str


class Route(RWSchema, BaseModel):
    id: uuid.UUID
    start_terminal: Terminal
    end_terminal: Terminal
