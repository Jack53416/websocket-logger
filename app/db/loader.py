from app.db.file_index import FileIndex
from app.schemas.database import Database


def load_db() -> Database:
    return Database(
        places_collection=FileIndex.PLACES.load(),
        trips=FileIndex.TRIPS.load(),
        trip_geometries=FileIndex.TRIP_GEOMETRIES.load().__root__,
        vehicle_locations=FileIndex.VEHICLES.load(),
        cities=FileIndex.CITIES.load().__root__,
        bus_stops=FileIndex.BUS_STOPS.load(),
    )
