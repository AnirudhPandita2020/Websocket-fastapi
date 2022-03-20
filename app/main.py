
import json
from app.Notifer import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse



manager = ConnectionManager()
app = FastAPI()




@app.websocket("/ws/{task_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket,task_id:int,user_id:str):
    await manager.connect(websocket,task_id,user_id)
    joined_message = {
                "message":"joined",
                "task_id":str(task_id),
                "user_id":user_id
            }
    await manager.broadcast(f"{joined_message}",task_id)
    print(manager.active_connections)
    try:
        while True:
            data = await websocket.receive_text()
            
            message_data = json.loads(data)
            print(message_data['message'])
            await manager.broadcast(f"{message_data}",task_id)
            #await manager.broadcast(f"{joined_message}",task_id)
    
    
    except WebSocketDisconnect:
        print(websocket)
        manager.disconnect(websocket,task_id,user_id)
        data = {
            "message":"left",
            "task_id":str(task_id),
            "user_id":user_id
        }
        message = json.dumps(data)
        print(manager.active_connections)
        #testing the file
        await manager.broadcast(message,task_id)
        
