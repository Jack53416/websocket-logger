import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Path

from app.api.utils import crud_utils
from app.api.utils.ride_simulator import RideSimulator
from app.db.database import get_db
from app.schemas.city import City
from app.schemas.database import Database
from app.schemas.geojson import PointGeometry, FeatureCollection
from app.schemas.quay import PlacesCollection
from app.schemas.ride import RideCollection, Ride
from app.schemas.trip import TripCollection, Trip

router = APIRouter()
ride_progress = 0
ride_increment = 0.05


@router.get('/places-collection/{phrase}',
            response_model=PlacesCollection)
def search_location(phrase: str,
                    db: Database = Depends(get_db)):
    return PlacesCollection.construct(
        quays=[quay for quay in db.places_collection.quays if phrase.lower() in quay.name.lower()]
    )


@router.post('/trips', response_model=list[Trip])
def find_trip(origin: str = Form(...),
              destination: str = Form(...),
              db: Database = Depends(get_db)):
    return db.trips


@router.get('/geometries/routes/{routeId}/quays/{quayId}', response_model=FeatureCollection)
def get_trip_geometry(route_id: uuid.UUID = Path(..., alias='routeId'),
                      quay_id: str = Path(..., alias='quayId'),
                      db: Database = Depends(get_db)):
    """
    Returns geometry for the provided route uuid. For mock purposes quay uuid is not used. If no geometry matches route
    uuid then first geometry is returned
    """

    return crud_utils.get_route_geometry(db, route_id=route_id)


@router.get("/vehicles/{vehicleId}/position", response_model=Ride)
def get_vehicle_position(db: Database = Depends(get_db),
                         vehicle_id: uuid.UUID = Path(..., alias='vehicleId'),
                         ride_simulator: RideSimulator = Depends(RideSimulator)):
    global ride_progress

    route_id = crud_utils.find_route_for_vehicle(db, vehicle_id=vehicle_id)
    ride_simulator.load_route(
        crud_utils.get_route_geometry(db, route_id=route_id)
    )

    ride = Ride(
        id=vehicle_id,
        position=PointGeometry(
            coordinates=ride_simulator.interpolate(ride_progress)

        )
    )

    def increment_progress(progress: float):
        progress = round(progress + ride_increment, 2)
        if progress > 1:
            return 0
        return progress

    ride_progress = increment_progress(ride_progress)
    return ride


@router.get('/cities', response_model=list[City])
def get_cities(db: Database = Depends(get_db)):
    return db.cities


@router.get('/quays', response_model=FeatureCollection)
def get_bus_stops(db: Database = Depends(get_db)):
    return db.bus_stops


@router.get('/quays/{quayId}/trips', response_model=list[Trip])
def get_trips_for_bus_stop(db: Database = Depends(get_db), quay_id: str = Path(..., alias='quayId')):
    return db.trips
