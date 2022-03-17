# Websocket-fastapi
A simple Realtime chat type system using Websockets and Fastapi

To Start:

1.clone the repository

2.Install the packages using pip install -r requirements.py

3.Run the code on the uvicorn server (uvicorn app.main:app --reload)

4.Open https://www.piesocket.com/websocket-tester to test the websocket

Note:
The format of the websocket url is as follows(Local machine) -> ws://localhost:8000/ws/{room_no}

The message will be broadcasted only to the websocket belonging to the {room_no}
