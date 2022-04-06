import json
import sys
from datetime import timedelta

from fastapi import FastAPI, Query
from loguru import logger
from starlette.websockets import WebSocket, WebSocketDisconnect

from connection_manager import ConnectionManager
from log import AppLogger

app = FastAPI()
manager = ConnectionManager()


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


@app.get("/hello")
def hello():
    return 'hello'


@app.websocket("/ws/{client_name}")
async def websocket_logger(websocket: WebSocket,
                           client_name: str,
                           compact_log: str = Query(True, alias='compactLog')):
    await manager.connect(websocket, client_name)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f'[{client_name}] got message:',
                         name='websocket-data',
                         payload=data if compact_log else json.loads(data))
    except WebSocketDisconnect:
        manager.disconnect(client_name)
