import uuid
from itertools import chain
from pathlib import Path
from typing import Iterable

from faker import Faker

from app.schemas.city import City, CitiesCollection
from app.schemas.database import Database
from app.schemas.geojson import FeatureCollection, PointGeometry
from app.schemas.quay import Quay, PlacesCollection
from app.schemas.ride import Ride, RideCollection
from app.schemas.trip import TripCollection

QUAYS_COUNT = 20
PLACES_FILE = 'places.json'
TRIPS_FILE = 'trips.json'
BUSES_FILE = 'buses.json'
CITIES_FILE = 'cities.json'
BUS_STOPS_FILE = 'bus-stops.json'

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

    with open(f'./sources/{CITIES_FILE}', 'w') as file:
        file.write(cities.json())


def create_bus_locations():
    points = [
        (19.462109, 51.712512),
        (19.420609, 51.773098),
        (19.340841, 51.811713)
    ]
    rides = [Ride(id=uuid.uuid4(), position=PointGeometry(coordinates=point)) for point in points]

    with open(f'./sources/{BUSES_FILE}', 'w') as file:
        file.write(
            RideCollection(rides=rides).json()
        )


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
            Path(f'app/db/sources/{TRIPS_FILE}').open('r') as trips_file, \
            Path(f'app/db/sources/{BUSES_FILE}').open('r') as buses_file, \
            Path(f'app/db/sources/{CITIES_FILE}').open('r') as cities_file, \
            Path(f'app/db/sources/{BUS_STOPS_FILE}').open('r') as bus_stops_file:
        return Database(
            places_collection=PlacesCollection.parse_raw(places_file.read()),
            trip_collection=TripCollection.parse_raw(trips_file.read()),
            bus_locations=RideCollection.parse_raw(buses_file.read()),
            cities=CitiesCollection.parse_raw(cities_file.read()).__root__,
            bus_stops=FeatureCollection.parse_raw(bus_stops_file.read()),
        )

# if __name__ == '__main__':
# create_cities()
# create_sources()
# assign_trip_bboxes()
