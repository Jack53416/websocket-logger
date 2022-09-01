from fastapi import APIRouter, Depends, Form

from app.db.database import get_db
from app.schemas.database import Database
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
