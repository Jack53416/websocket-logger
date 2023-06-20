import random
import uuid

from fastapi import APIRouter, Depends, Form, Path

from app.api.utils import crud_utils
from app.api.utils.ride_simulator import RideSimulator
from app.db import factories
from app.db.database import get_db
from app.schemas.city import City
from app.schemas.database import Database
from app.schemas.geojson import PointGeometry, FeatureCollection
from app.schemas.quay import PlacesCollection
from app.schemas.route import Route
from app.schemas.trip import Trip
from app.schemas.vehicle import Vehicle, VehicleEta

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


@router.get('/geometries/routes/{routeId}/start-quay/{quayId}', response_model=FeatureCollection)
def get_trip_geometry_to_route_end(route_id: uuid.UUID = Path(..., alias='routeId'),
                                   quay_id: str = Path(..., alias='quayId'),
                                   db: Database = Depends(get_db)):
    """
    Returns geometry for the provided route uuid. It is meant for the trips that last till te end of route starting
    on a provided start quay. For mock purposes quay ids do not have any impact on returned data.
    If no geometry matches route uuid then first geometry is returned
    """

    return crud_utils.get_route_geometry(db, route_id=route_id)


@router.get('/geometries/routes/{routeId}/start-quay/{startQuayId}/end-quay/{endQuayId}',
            response_model=FeatureCollection)
def get_trip_geometry(route_id: uuid.UUID = Path(..., alias='routeId'),
                      start_quay_id: str = Path(..., alias='startQuayId'),
                      end_quay_id: str = Path(..., alias='endQuayId'),
                      db: Database = Depends(get_db)):
    """
    Returns geometry for the provided route uuid. Start and end quays are used to determine metadata of the route
    geometry like its color on the map. For mock purposes quay ids do not have any impact on returned data.
    If no geometry matches route uuid then first geometry is returned
    """

    return crud_utils.get_route_geometry(db, route_id=route_id)


@router.get("/vehicles/{vehicleId}/position", response_model=Vehicle)
def get_vehicle_position(db: Database = Depends(get_db),
                         vehicle_id: uuid.UUID = Path(..., alias='vehicleId'),
                         ride_simulator: RideSimulator = Depends(RideSimulator)):
    global ride_progress

    trip = crud_utils.find_trip_for_vehicle(db, vehicle_id=vehicle_id)
    ride_simulator.load_route(
        crud_utils.get_route_geometry(db, route_id=trip.route.id)
    )

    eta_step = random.randrange(10, 500)
    vehicle = Vehicle(
        id=vehicle_id,
        position=PointGeometry(
            coordinates=ride_simulator.interpolate(ride_progress)

        ),
        eta=[VehicleEta(quay_id=quay.id, eta=eta) for quay, eta in
             zip(trip.quays, range(100, (len(trip.quays) + 1) * eta_step, eta_step))]
    )

    def increment_progress(progress: float):
        progress = round(progress + ride_increment, 2)
        if progress > 1:
            return 0
        return progress

    ride_progress = increment_progress(ride_progress)
    return vehicle


@router.get('/routes/{routeId}', response_model=Route)
def get_route_detail(route_id: uuid.UUID = Path(..., alias='routeId')):
    return factories.get_route()


@router.get('/cities', response_model=list[City])
def get_cities(db: Database = Depends(get_db)):
    return db.cities


@router.get('/quays', response_model=FeatureCollection)
def get_bus_stops(db: Database = Depends(get_db)):
    return db.bus_stops


@router.get('/quays/{quayId}/trips', response_model=list[Trip])
def get_trips_for_bus_stop(db: Database = Depends(get_db), quay_id: str = Path(..., alias='quayId')):
    return db.trips
