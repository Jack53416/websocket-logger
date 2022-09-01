from fastapi import APIRouter

from app.api.enpoints import driver, transit

api_router = APIRouter()

api_router.include_router(driver.router, prefix='/driver', tags=['driver'])
api_router.include_router(transit.router, prefix='/transit', tags=['transit'])


@api_router.get("/hello")
def hello():
    return 'hello'
