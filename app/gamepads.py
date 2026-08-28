import asyncio
import vgamepad as vg
from app.buttons import buttons_handler
from app.triggers import triggers_handler
from app.joysticks import joysticks_handler

controllers = {}


def create_controller(gamepad_id, websocket, loop):
    controller = vg.VX360Gamepad()

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

    controller.register_notification(callback_function=vibration_callback)

    return controller


def gamepad_handler(gamepad, data):
    buttons_handler(gamepad, data["buttons"])
    triggers_handler(gamepad, data["triggers"])
    joysticks_handler(gamepad, data["joysticks"])
    gamepad.update()


def gamepads_handler(gamepads, websocket, loop):
    active_ids = set()

    for data in gamepads:
        gamepad_id = data["id"]
        active_ids.add(gamepad_id)

        if gamepad_id not in controllers:
            controllers[gamepad_id] = create_controller(gamepad_id, websocket, loop)

        gamepad_handler(controllers[gamepad_id], data)

    for gamepad_id in list(controllers):
        if gamepad_id not in active_ids:
            del controllers[gamepad_id]
