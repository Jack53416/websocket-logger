from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


def register_middlewares(app: FastAPI):
    app.middleware('http')(catch_exceptions_middleware)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logger.exception('Unhandled exception occurred')
        error = jsonable_encoder({'error': 'Something went wrong'})
        return JSONResponse(content=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
