import uuid

from pydantic import BaseModel

from app.schemas.city import City
from app.schemas.geojson import FeatureCollection
from app.schemas.quay import PlacesCollection
from app.schemas.trip import TripCollection


class Database(BaseModel):
    places_collection: PlacesCollection
    trip_collection: TripCollection
    trip_geometries: dict[uuid.UUID, FeatureCollection]
    cities: list[City]
    bus_stops: FeatureCollection
