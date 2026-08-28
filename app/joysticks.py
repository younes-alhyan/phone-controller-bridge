from app.utils import apply_dead_zone, apply_invert


def joystick_handler(gamepad, joystick, index):
    x = apply_dead_zone(joystick["x"]["value"], joystick["dead_zone"])
    x = apply_invert(x, joystick["x"]["invert"])

    y = apply_dead_zone(joystick["y"]["value"], joystick["dead_zone"])
    y = apply_invert(y, joystick["y"]["invert"])

    if index == 0:
        gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
    elif index == 1:
        gamepad.right_joystick_float(x_value_float=x, y_value_float=y)


def joysticks_handler(gamepad, joysticks):
    for index, joystick in enumerate(joysticks):
        joystick_handler(gamepad, joystick, index)
