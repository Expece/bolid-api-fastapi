from sqlalchemy.orm import Session

from app.db.models import Sensor
from app.sensors.schema import SensorInDB

def parse_sensors(db: Session) -> list[SensorInDB]:
    """Return sensors from database in view like list[SensorInDB]"""
    all_sensors = db.query(Sensor).all()
    parsed_sensors = []
    for sensor in all_sensors:
        parsed_sensors.append(
            SensorInDB(
                id=sensor.id,
                name=sensor.name,
                type=sensor.type
            )
        )
    return parsed_sensors