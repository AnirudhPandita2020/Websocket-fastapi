
from app.Notifer import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()


manager = ConnectionManager()


@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket,task_id:int):
    await manager.connect(websocket,task_id)
    #print(task_id,manager.active_connections)
    try:
        while True:
            data = await websocket.receive_text()
            
            await manager.broadcast(f"{data}",task_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket,task_id)
        
        await manager.broadcast("left",task_id)
