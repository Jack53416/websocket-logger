import random
import uuid

from fastapi import APIRouter, Depends, Form

from app.db.database import get_db
from app.schemas.bus import BusCollection, GeoPoint
from app.schemas.database import Database
from app.schemas.geojson import FeatureCollection
from app.schemas.quay import PlacesCollection
from app.schemas.trip import TripCollection

router = APIRouter()


@router.get('/places-collection/{phrase}',
            response_model=PlacesCollection)
def search_location(phrase: str,
                    db: Database = Depends(get_db)):
    return PlacesCollection.construct(
        quays=[quay for quay in db.places_collection.quays if phrase.lower() in quay.name.lower()]
    )


@router.post('/trips', response_model=TripCollection)
def find_trip(origin: str = Form(...),
              destination: str = Form(...),
              db: Database = Depends(get_db)):
    return db.trip_collection


@router.get("/rides/{id}", response_model=BusCollection)
def get_buses_positions(id: str, db: Database = Depends(get_db)):
    value = random.randrange(1, 5)
    sign = random.choice([-1, 1])
    difference = (value / 100) * sign
    buses = [
        GeoPoint(
            latitude=round(bus.latitude + difference, 5),
            longitude=round(bus.longitude + difference, 5)
        ) for bus in db.bus_locations.buses
    ]

    return BusCollection(buses=buses)
