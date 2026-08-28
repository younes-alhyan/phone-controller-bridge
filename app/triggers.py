from app.utils import apply_threshold


def trigger_handler(gamepad, trigger, index):
    value = apply_threshold(trigger["value"], trigger["threshold"])
    if index == 0:
        gamepad.left_trigger(value=int(value * 255))
    elif index == 1:
        gamepad.right_trigger(value=int(value * 255))


def triggers_handler(gamepad, triggers):
    for index, trigger in enumerate(triggers):
        trigger_handler(gamepad, trigger, index)
