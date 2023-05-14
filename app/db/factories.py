import uuid
from itertools import chain
from pathlib import Path
from typing import Iterable

from faker import Faker

from app.db.file_index import FileIndex
from app.schemas.city import City, CitiesCollection
from app.schemas.geojson import FeatureCollection, PointGeometry
from app.schemas.quay import Quay, PlacesCollection
from app.schemas.ride import Ride, RideCollection
from app.schemas.trip import TripCollection

fake = Faker()


def create_cities():
    model_fields = City.schema()['required']

    raw_data = [
        ('Warsaw', 'Poland', 'PL', [20.851688337, 52.097849613, 21.271151294, 52.368153945]),
        ('Lodz', 'Poland', 'PL', [19.3208619, 51.686144256, 19.63994302, 51.859919288]),
        ('München', 'Germany', 'DE', [11.360781, 48.061596, 11.722879, 48.248216]),
        ('Nairobi', 'Kenya', 'KE', [36.664464, -1.445609, 37.104955, -1.160583])
    ]

    cities: CitiesCollection = CitiesCollection(__root__=[
        City(**dict(zip(model_fields, record))) for record in raw_data
    ])

    with open(f'./sources/{FileIndex.CITIES}', 'w') as file:
        file.write(cities.json())


def create_bus_locations():
    points = [
        (19.462109, 51.712512),
        (19.420609, 51.773098),
        (19.340841, 51.811713)
    ]
    rides = [Ride(id=uuid.uuid4(), position=PointGeometry(coordinates=point)) for point in points]

    with open(f'./sources/{FileIndex.VEHICLES}', 'w') as file:
        file.write(
            RideCollection(rides=rides).json()
        )


def create_places():
    QUAYS_COUNT = 20

    quays = [
        Quay(
            id=uuid.uuid4(),
            name=fake.street_name()
        ) for _ in range(0, QUAYS_COUNT)
    ]

    with open(f'./sources/{FileIndex.PLACES}', 'w') as file:
        file.write(
            PlacesCollection(
                quays=quays
            ).json())


def assign_trip_bboxes():
    with Path(f'./sources/{FileIndex.TRIPS}').open('r') as trip_file:
        trip_collection = TripCollection.parse_raw(trip_file.read())

    for trip_part in (trip_part for trip in trip_collection.trips for trip_part in trip.trip_parts):
        trip_part.route_geometry.bbox = compute_trip_bbox(trip_part.route_geometry)

    with Path(f'./sources/{FileIndex.TRIPS}').open('w') as trip_file:
        trip_file.write(trip_collection.json())


def compute_trip_bbox(feature_collection: FeatureCollection):
    coordinates = chain.from_iterable(feature.geometry.coordinates for feature in feature_collection.features)
    points = (point for point in coordinates if isinstance(point, Iterable))
    south_bound, north_bound = [bound_point for bound_point in zip(*[(min(axis), max(axis)) for axis in zip(*points)])]
    return [*south_bound, *north_bound]
