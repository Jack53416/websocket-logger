import uuid

from fastapi import APIRouter, Depends, Form, Path

from app.api.utils.RideSimulator import RideSimulator
from app.db.database import get_db
from app.schemas.database import Database
from app.schemas.geojson import PointGeometry
from app.schemas.quay import PlacesCollection
from app.schemas.ride import RideCollection, Ride
from app.schemas.trip import TripCollection

router = APIRouter()
ride_progress = [0, 0.5, 0.8]
ride_increment = 0.05


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


@router.get("/route/{routeId}/rides", response_model=RideCollection)
def get_buses_positions(db: Database = Depends(get_db),
                        route_id: str = Path(..., alias='routeId'),
                        ride_simulator: RideSimulator = Depends(RideSimulator)):
    global ride_progress
    ride_simulator.load_route(db.trip_collection.trips[0].trip_parts[0].route_geometry)
    rides = [
        Ride(
            id=uuid.uuid4(),
            position=PointGeometry(
                coordinates=ride_simulator.interpolate(ride)

            )
        )
        for ride in ride_progress
    ]

    def increment_progress(progress):
        progress = round(progress + ride_increment, 2)
        if progress > 1:
            return 0
        return progress

    ride_progress = list(map(increment_progress, ride_progress))
    return RideCollection(rides=rides)
