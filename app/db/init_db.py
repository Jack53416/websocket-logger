import uuid
from pathlib import Path

from faker import Faker

from app.schemas.database import Database
from app.schemas.quay import Quay, PlacesCollection
from app.schemas.trip import TripCollection

QUAYS_COUNT = 20

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

    with open('./sources/places.json', 'w') as file:
        file.write(
            PlacesCollection(
                quays=quays
            ).json())


def load_db() -> Database:
    with Path('app/db/sources/places.json').open('r') as places_file, \
            Path('app/db/sources/trips.json').open('r') as trips_file:
        return Database(
            places_collection=PlacesCollection.parse_raw(places_file.read()),
            trip_collection=TripCollection.parse_raw(trips_file.read())
        )


if __name__ == '__main__':
    create_sources()
