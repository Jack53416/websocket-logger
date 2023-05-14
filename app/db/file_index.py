import dataclasses
from enum import Enum
from pathlib import Path
from typing import Generic, TypeVar, Type

from pydantic import BaseModel

from app.schemas.geojson import FeatureCollection
from app.schemas.quay import PlacesCollection
from app.schemas.trip import TripCollection, TripGeometryCollection
from app.schemas.ride import RideCollection
from app.schemas.city import CitiesCollection

BASE_PATH = Path('app/db/sources')
T = TypeVar("T", bound=BaseModel)


@dataclasses.dataclass()
class DbFile(Generic[T]):
    __slots__ = ['file', 'model']
    file: str
    model: Type[T]

    @property
    def path(self) -> Path:
        return BASE_PATH / self.file

    def __str__(self) -> str:
        return self.file

    def load(self) -> T:
        with open(self.path, 'r') as model_file:
            return self.model.parse_raw(model_file.read())


class FileIndex(object):
    PLACES = DbFile('places.json', PlacesCollection)
    TRIPS = DbFile('trips/trips.json', TripCollection)
    TRIP_GEOMETRIES = DbFile('trips/geometries.json', TripGeometryCollection)

    VEHICLES = DbFile('trips/vehicles.json', RideCollection)
    CITIES = DbFile('cities.json', CitiesCollection)
    BUS_STOPS = DbFile('bus-stops.json', FeatureCollection)
