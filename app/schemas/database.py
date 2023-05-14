import uuid
from typing import List

from pydantic import BaseModel

from app.schemas.city import City
from app.schemas.geojson import FeatureCollection
from app.schemas.quay import PlacesCollection
from app.schemas.ride import RideCollection
from app.schemas.trip import TripCollection


class Database(BaseModel):
    places_collection: PlacesCollection
    trips: TripCollection
    trip_geometries: dict[uuid.UUID, FeatureCollection]
    vehicle_locations: RideCollection
    cities: List[City]
    bus_stops: FeatureCollection
