
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.WebSocketManager import WebSocketManager

app = FastAPI(
    title="Realtime chat"
)

broadcast = WebSocketManager()


@app.on_event("startup")
async def startBroadcast():
    await broadcast.connectService()


@app.on_event("shutdown")
async def closeBroadcast():
    await broadcast.disconnectService()



@app.websocket("/ws/{task_id}/{user_id}")
async def get_Connection(webSocket:WebSocket,task_id:int,user_id:str):
    try:
        
        await broadcast.chatroom_ws(webSocket,task_id,user_id)
      
    except WebSocketDisconnect as e:
        print("Left {}".format(webSocket))