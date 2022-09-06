import uuid
from itertools import chain
from pathlib import Path
from typing import Iterable

from faker import Faker

from app.schemas.database import Database
from app.schemas.geojson import FeatureCollection
from app.schemas.quay import Quay, PlacesCollection
from app.schemas.trip import TripCollection

QUAYS_COUNT = 20
PLACES_FILE = 'places.json'
TRIPS_FILE = 'trips.json'

fake = Faker()


def create_sources():
    create_places()


def create_places():
    quays = [
        Quay(
            id=uuid.uuid4(),
            name=fake.street_name()
        ) for _ in range(0, QUAYS_COUNT)
    ]

    with open(f'./sources/{PLACES_FILE}', 'w') as file:
        file.write(
            PlacesCollection(
                quays=quays
            ).json())


def assign_trip_bboxes():
    with Path(f'./sources/{TRIPS_FILE}').open('r') as trip_file:
        trip_collection = TripCollection.parse_raw(trip_file.read())

    for trip_part in (trip_part for trip in trip_collection.trips for trip_part in trip.trip_parts):
        trip_part.route_geometry.bbox = compute_trip_bbox(trip_part.route_geometry)

    with Path(f'./sources/{TRIPS_FILE}').open('w') as trip_file:
        trip_file.write(trip_collection.json())


def compute_trip_bbox(feature_collection: FeatureCollection):
    coordinates = chain.from_iterable(feature.geometry.coordinates for feature in feature_collection.features)
    points = (point for point in coordinates if isinstance(point, Iterable))
    south_bound, north_bound = [bound_point for bound_point in zip(*[(min(axis), max(axis)) for axis in zip(*points)])]
    return [*south_bound, *north_bound]


def load_db() -> Database:
    with Path(f'app/db/sources/{PLACES_FILE}').open('r') as places_file, \
            Path(f'app/db/sources/{TRIPS_FILE}').open('r') as trips_file:
        return Database(
            places_collection=PlacesCollection.parse_raw(places_file.read()),
            trip_collection=TripCollection.parse_raw(trips_file.read())
        )


if __name__ == '__main__':
    create_sources()
    assign_trip_bboxes()
