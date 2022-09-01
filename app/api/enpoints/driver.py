import json

from fastapi import APIRouter, Query
from loguru import logger
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.core.ws.connection_manager import ConnectionManager

manager = ConnectionManager()
router = APIRouter()


@router.websocket("/ws/{client_name}", name='ws:logger')
async def websocket_logger(websocket: WebSocket,
                           client_name: str,
                           compact_log: str = Query(True, alias='compactLog')):
    await manager.connect(websocket, client_name)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f'[{client_name}] got message:',
                        name='websocket-data',
                        payload=data if compact_log else json.loads(data))
    except WebSocketDisconnect:
        manager.disconnect(client_name)
