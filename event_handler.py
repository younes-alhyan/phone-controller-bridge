import pyvjoy
import logging
from config import button_map, trigger_map, stick_axis_map, dpad_axis_map,TRIGGER_THRESHOLD
from utils import scale_to_vjoy, parse_dpad_value

# Create a vJoy device instance (simulate virtual controller)
vjoy = pyvjoy.VJoyDevice(1)

def handle_event(code, value):
    """Handle one event and update vJoy state accordingly."""
    try:
        if code in button_map:
            vjoy.set_button(button_map[code], value != 0)

        elif code in trigger_map:
            vjoy.set_button(trigger_map[code], value >= TRIGGER_THRESHOLD)

        elif code in stick_axis_map:
            vjoy.set_axis(stick_axis_map[code], scale_to_vjoy(value))

        elif code in dpad_axis_map:
            for btn in parse_dpad_value(code, value):
                vjoy.set_button(btn["id"], btn["state"])

    except Exception as e:
        logging.error(f"Error handling event: {e}")
