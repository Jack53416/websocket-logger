import uuid

from fastapi import Depends

from app.db.database import get_db
from app.schemas.database import Database
from app.schemas.geojson import FeatureCollection
from app.schemas.trip import Trip


def get_route_geometry(db: Database, *, route_id: uuid.UUID) -> FeatureCollection:
    if geometry := db.trip_geometries.get(route_id):
        return geometry

    return next(iter(db.trip_geometries.values()))


def find_route_for_vehicle(db: Database, *, vehicle_id: uuid.UUID) -> uuid.UUID:
    trip = next((trip for trip in db.trips if trip.vehicle.id == vehicle_id), db.trips[0])
    return trip.route.id
