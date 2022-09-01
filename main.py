import sys
from datetime import timedelta

import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.api.api import api_router
from app.core.config import settings
from app.core.log import AppLogger
from app.core.middleware import register_middlewares

app = FastAPI()
register_middlewares(app)
app.include_router(api_router)


@app.on_event('startup')
def startup():
    AppLogger.make_logger({
        'sink': sys.stderr,
        'level': 'DEBUG',
        'backtrace': False,
        'diagnose': False,
        'enqueue': True
    }, {
        'sink': './logs/websocket.log',
        'level': 'DEBUG',
        'rotation': '100 MB',
        'filter': lambda record: record['extra'].get('name') == 'websocket-data',
        'retention': timedelta(hours=8),
        'backtrace': False,
        'diagnose': False,
        'enqueue': True
    })
    logger.info("Server started")


if __name__ == '__main__':
    uvicorn.run('main:app', host=str(settings.SERVER_HOST), port=settings.SERVER_PORT, reload=True)
