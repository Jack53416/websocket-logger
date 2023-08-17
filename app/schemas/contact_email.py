from pydantic import BaseModel

from app.schemas.common.base import RWSchema


class ContactEmail(RWSchema, BaseModel):
    name: str
    email: str
    subject: str
    text: str
