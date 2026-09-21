import asyncio
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.gamepads import gamepads_handler

app = FastAPI()


@app.get("/")
async def index():
    return FileResponse("static/index.html")


connections = {}


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    connection_id = str(uuid.uuid4())
    connections[connection_id] = {"websocket": websocket, "gamepads": {}}

    loop = asyncio.get_running_loop()
    try:
        while True:
            gamepads = await websocket.receive_json()
            gamepads_handler(connections[connection_id], gamepads, loop)

    except WebSocketDisconnect:
        connections.pop(connection_id, None);


app.mount("/static", StaticFiles(directory="static"), name="static")
