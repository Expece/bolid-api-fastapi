

def check_sensor_type(sensor_type) -> bool:
    types = [1, 2, 3]
    if sensor_type not in types:
        return False
    return True
