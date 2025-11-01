# Device path for the controller (via ADB)
controller_device_path = "/dev/input/event7"

# Only accept these types of events
accepted_event_types = [0x01, 0x03]

# Mappings for various controller parts
button_map = {
    0x130: 1,   # Cross
    0x131: 2,   # Circle
    0x133: 3,   # Triangle
    0x134: 4,   # Square
    0x136: 5,   # L1
    0x137: 6,   # R1
    0x13a: 9,   # Share
    0x13b: 10,  # Options
    0x13c: 11,  # PS
    0x13d: 12,  # L3
    0x13e: 13   # R3
}

trigger_map = {
    0x02: 7,  # L2
    0x05: 8   # R2
}

stick_axis_map = {
    0x00: 48,   # Left Stick X
    0x01: 49,   # Left Stick Y
    0x03: 51,  # Right Stick X
    0x04: 52   # Right Stick Y
}

dpad_axis_map = {
    0x10: "Dpad LR",  # Left/Right
    0x11: "Dpad UD"   # Up/Down
}

dpad_buttons = {
    "up": 14,
    "right": 15,
    "down": 16,
    "left": 17
}

VJOY_SCALE = 32768  # You can move this to the CONFIG file for easier adjustment

TRIGGER_THRESHOLD = 100