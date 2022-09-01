from typing import Dict

from starlette.websockets import WebSocket


class ConnectionManager(object):
    LOG_GUI = 'LOG_GUI'

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_name: str):
        await websocket.accept()
        self.active_connections[client_name] = websocket

    def disconnect(self, client_name: str):
        if client_name in self.active_connections:
            self.active_connections.pop(client_name)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    @staticmethod
    async def send_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)
