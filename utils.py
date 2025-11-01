from config import dpad_buttons,VJOY_SCALE 

def scale_to_vjoy(value_0_255):
    """Scale input value from 0-255 to vJoy's 0-32768 range."""
    if 0 <= value_0_255 <= 255:
        return int((value_0_255 / 255) * VJOY_SCALE)
    raise ValueError("Input value must be between 0 and 255")

def parse_dpad_value(code, value):
    """Returns a list of D-Pad button states based on raw axis input."""
    axis_buttons = (
        [dpad_buttons["left"], dpad_buttons["right"]] if code == 0x10
        else [dpad_buttons["up"], dpad_buttons["down"]]
    )
    result = []
    if value == 0:
        for btn in axis_buttons:
            result.append({"id": btn, "state": False})
    elif value > 1:
        result.append({"id": axis_buttons[0], "state": True})
    else:
        result.append({"id": axis_buttons[1], "state": True})
    return result
