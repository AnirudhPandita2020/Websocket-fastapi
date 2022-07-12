import json
from re import sub
from unittest import async_case
from broadcaster import Broadcast
from fastapi import WebSocket
from fastapi.concurrency import run_until_first_complete


class WebSocketManager(object):
    def __init__(self):
        self.broadcast = Broadcast("memory://")
        
    
    async def connectService(self):
        await self.broadcast.connect()
        
    async def disconnectService(self):
        await self.broadcast.disconnect()

    async def chatroom_ws(self,websocket:WebSocket,task_id,user_id):
        await websocket.accept()
        await run_until_first_complete(
            (self.chatroom_ws_receiver, {"websocket": websocket,"task_id":task_id}),
            (self.chatroom_ws_sender, {"websocket": websocket,"task_id":task_id}),
        )


    async def chatroom_ws_receiver(self,websocket:WebSocket,task_id):
        async for message in websocket.iter_text():
            await self.broadcast.publish(channel=str(task_id), message=message)


    async def chatroom_ws_sender(self,websocket:WebSocket,task_id):
        async with self.broadcast.subscribe(channel=str(task_id)) as subscriber:
            async for event in subscriber:
                await websocket.send_text(event.message)

    
    async def sendJoinMessage(self,websocket:WebSocket,task_id,user_id):
        async with self.broadcast.subscribe(channel=str(task_id)) as subscriber:
            async for event in subscriber:
                await websocket.send_text(json.dumps(
                     {
                "message":"joined",
                "task_id":str(task_id),
                "user_id":user_id
            }
                ))