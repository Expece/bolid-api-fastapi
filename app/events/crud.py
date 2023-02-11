from .forms import RequestEvents, EventForm
from sqlalchemy.orm import Session
from app.db.models import Event

# -------------------------------------------------------------
from app.db.models import Sensor
from app.sensors.crud import create_sensor, get_sensor_by_id

def check_exist_or_create_sensor(db: Session, id: int):
    if not get_sensor_by_id(db, id):
        create_sensor(db, sensor=Sensor(name=None, type=1))
# -------------------------------------------------------------

def create_event(db: Session, import_events: RequestEvents):
    for event in import_events.events:
        check_exist_or_create_sensor(db, event.sensor_id)
        event = Event(sensor_id=event.sensor_id, name=event.name,
        temperature=event.temperature, humidity=event.humidity)
        db.add(event)
    db.commit()
    return import_events


def get_event_by_id(db: Session, id: int):
    return db.query(Event).filter(Event.id == id).first()


def get_events(db: Session, skip: int, limit: int):
    return db.query(Event).offset(skip).limit(limit).all()


def updare_event(db: Session, id:int, event: EventForm):
    db.query(Event).filter(Event.id == id).update({
        'sensor_id': event.sensor_id,
        'name': event.name,
        'temperature': event.temperature,
        'humidity': event.humidity
    })
    db.commit()
    return event


def delete_event(db: Session, id: int):
    event = get_event_by_id(db, id)
    db.delete(event)
    db.commit()