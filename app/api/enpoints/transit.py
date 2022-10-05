import random
from typing import List

from fastapi import APIRouter, Depends, Form, Query

from app.db.database import get_db
from app.schemas.database import Database
from app.schemas.geojson import PointGeometry
from app.schemas.quay import PlacesCollection
from app.schemas.ride import RideCollection, Ride
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


@router.get("/rides", response_model=RideCollection)
def get_buses_positions(db: Database = Depends(get_db), rides: List[str] = Query(...)):
    value = random.randrange(1, 5)
    sign = random.choice([-1, 1])
    difference = (value / 1000) * sign

    rides = [
        Ride(
            id=ride.id,
            position=PointGeometry(
                coordinates=tuple(map(lambda coord: round(coord + difference, 5), ride.position.coordinates))

            )
        )
        for ride in db.bus_locations.rides
    ]

    return RideCollection(rides=rides)
