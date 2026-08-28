def apply_dead_zone(value, dead_zone_percent):
    dead_zone = dead_zone_percent / 100

    if abs(value) < dead_zone:
        return 0.0

    return value


def apply_invert(value, invert):
    return -value if invert else value


def apply_threshold(value, threshold_percent):
    threshold = threshold_percent / 100

    if threshold >= 1:
        return 1.0 if value >= 1 else 0.0

    if value <= threshold:
        return 0.0

    return (value - threshold) / (1 - threshold)
