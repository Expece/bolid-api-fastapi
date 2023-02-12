from .schema import RequestEvent, EventSchema
from sqlalchemy.orm import Session
from fastapi_pagination import Params, paginate

from app.db.models import Event
from app.events.utils import check_exist_or_create_sensor, parse_events


def create_event(db: Session, import_events: RequestEvent):
    for event in import_events.events:
        check_exist_or_create_sensor(db, event.sensor_id)
        _event = Event(sensor_id=event.sensor_id, name=event.name,
        temperature=event.temperature, humidity=event.humidity)
        db.add(_event)
    db.commit()


def get_event_by_id(db: Session, id: int):
    return db.query(Event).filter(Event.id == id).first()


def get_all_events(db: Session, params: Params):
    return paginate(parse_events(db), params)


def updare_event(db: Session, id:int, event: EventSchema):
    db.query(Event).filter(Event.id == id).update({
        'sensor_id': event.sensor_id,
        'name': event.name,
        'temperature': event.temperature,
        'humidity': event.humidity
    })
    db.commit()


def delete_event(db: Session, id: int):
    event = get_event_by_id(db, id)
    db.delete(event)
    db.commit()