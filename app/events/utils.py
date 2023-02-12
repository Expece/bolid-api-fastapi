from sqlalchemy.orm import Session

from app.db.models import Sensor, Event
from app.events.schema import EventInDB
from app.sensors.crud import create_sensor, get_sensor_by_id


def check_exist_or_create_sensor(db: Session, id: int):
    if not get_sensor_by_id(db, id):
        create_sensor(db, sensor=Sensor(name=None))


def parse_events(db: Session) -> list[EventInDB]:
    """Return events from database in view like list[EventInDB]"""
    all_events = db.query(Event).all()
    parsed_events = []
    for event in all_events:
        parsed_events.append(
            EventInDB(
                id=event.id,
                sensor_id=event.sensor_id,
                name=event.name,
                temperature=event.temperature,
                humidity=event.humidity
            )
        )
    return parsed_events