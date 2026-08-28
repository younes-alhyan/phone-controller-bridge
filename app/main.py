import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.gamepads import gamepads_handler

app = FastAPI()


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()

    loop = asyncio.get_running_loop()
    try:
        while True:
            gamepads = await websocket.receive_json()
            gamepads_handler(gamepads, websocket, loop)

    except WebSocketDisconnect:
        print("WebSocket disconnected")


app.mount("/static", StaticFiles(directory="static"), name="static")
