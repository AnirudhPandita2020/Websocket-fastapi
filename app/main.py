
import json
from app.Notifer import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var task_id = window.location.pathname
            var ws = new WebSocket(`ws://localhost:8000/ws`+task_id);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
app = FastAPI()

@app.get("/{task_id}/{user_id}")
async def get():
    return HTMLResponse(html)


manager = ConnectionManager()



@app.websocket("/ws/{task_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket,task_id:int,user_id:str):
    await manager.connect(websocket,task_id,user_id)
    joined_message = {
                "message":"joined",
                "task_id":str(task_id),
                "user_id":user_id
            }
    await manager.broadcast(f"{joined_message}",task_id)
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
        await manager.broadcast(message,task_id)
