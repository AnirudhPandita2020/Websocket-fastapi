from collections import defaultdict
from fastapi import WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = defaultdict(list)

    async def connect(self, websocket: WebSocket,task_id:int,user_id):
        await websocket.accept()
        if self.active_connections[task_id] is None:
            self.active_connections[task_id] = []
        else:
            self.active_connections[task_id].append([websocket,user_id])
            
    def disconnect(self, websocket: WebSocket,task_id:int,user_id:str):
        index = self.active_connections[task_id].index([websocket,user_id])
        self.active_connections[task_id].pop(index)
        

    async def send_personal_message(self, message: str, websocket: WebSocket,task_id:int):
        await websocket.send_text(message)

    async def broadcast(self, message: str,task_id:int):
        for connection in self.active_connections[task_id]:
            await connection[0].send_text(message)
            

