from collections import defaultdict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = defaultdict(list)

    async def connect(self, websocket: WebSocket,task_id:int):
        await websocket.accept()
        if self.active_connections[task_id] is None:
            self.active_connections[task_id] = []
        else:
            self.active_connections[task_id].append(websocket)
            
    def disconnect(self, websocket: WebSocket,task_id:int):
        self.active_connections[task_id].remove(websocket)
        if len(self.active_connections[task_id]) == 0:
            self.active_connections.pop(task_id)

    async def send_personal_message(self, message: str, websocket: WebSocket,task_id:int):
        await websocket.send_text(message)

    async def broadcast(self, message: str,task_id:int):
        for connection in self.active_connections[task_id]:
            await connection.send_text(message)
