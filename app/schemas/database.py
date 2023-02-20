from typing import List

from pydantic import BaseModel

from app.schemas.city import City
from app.schemas.quay import PlacesCollection
from app.schemas.ride import RideCollection
from app.schemas.trip import TripCollection


class Database(BaseModel):
    places_collection: PlacesCollection
    trip_collection: TripCollection
    bus_locations: RideCollection
    cities: List[City]
