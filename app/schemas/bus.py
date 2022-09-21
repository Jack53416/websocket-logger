from typing import List

from pydantic import BaseModel


class GeoPoint(BaseModel):
    longitude: float
    latitude: float


class BusCollection(BaseModel):
    buses: List[GeoPoint] = []
