from pydantic import BaseModel

from app.schemas.bus import BusCollection
from app.schemas.quay import PlacesCollection
from app.schemas.trip import TripCollection


class Database(BaseModel):
    places_collection: PlacesCollection
    trip_collection: TripCollection
    bus_locations: BusCollection | None
