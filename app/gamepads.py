import asyncio
import vgamepad as vg
from app.buttons import buttons_handler
from app.triggers import triggers_handler
from app.joysticks import joysticks_handler


def create_gamepad(gamepad_id, websocket, loop):
    gamepad = vg.VX360Gamepad()

    def vibration_callback(
        client, target, large_motor, small_motor, led_number, user_data
    ):
        data = {
            "type": "rumble",
            "id": gamepad_id,
            "strong": large_motor / 255,
            "weak": small_motor / 255,
        }
        asyncio.run_coroutine_threadsafe(websocket.send_json(data), loop)

    gamepad.register_notification(callback_function=vibration_callback)
    return gamepad


def gamepad_handler(gamepad, data):
    buttons_handler(gamepad, data["buttons"])
    triggers_handler(gamepad, data["triggers"])
    joysticks_handler(gamepad, data["joysticks"])
    gamepad.update()


def gamepads_handler(connection, gamepads, loop):
    active_ids = set()

    for data in gamepads:
        gamepad_id = data["id"]
        active_ids.add(gamepad_id)       

        if gamepad_id not in connection["gamepads"]:
            gamepad = create_gamepad(gamepad_id, connection["websocket"], loop)
            connection["gamepads"][gamepad_id] = gamepad

        gamepad_handler(connection["gamepads"][gamepad_id], data)

    for gamepad_id in list(connection["gamepads"]):
        if gamepad_id not in active_ids:
            del connection["gamepads"][gamepad_id]
