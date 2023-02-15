from .schema import RequestEvents, EventSchema
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Params
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.sql.expression import select

from app.db.models import Event
from app.crud_base import BaseCRUD
from app.events.filter import EventFilter
from app.sensors.sensor_service import sensors_service
from app.sensors.schema import SensorSchema


class EventServise(BaseCRUD[Event]):
    """Class for interacting with an Event table in a database"""

    def create(self, db: Session, event: EventSchema) -> None:
        """Create event. If there is no sensor
        associated with the event creates it."""
        self._check_exist_or_create_sensor(db, event.sensor_id)
        super().create(db, event)

    def create_multi(self, db: Session, events: RequestEvents) -> None:
        """Create multi events. If there is no sensor
        associated with the event creates it"""
        for event in events.events:
            self._check_exist_or_create_sensor(db, event.sensor_id)
            _event = jsonable_encoder(event)
            db.add(self.model(**_event))
        db.commit()
    

    def get_all(self, db: Session, params: Params) -> dict:
        """Get all events. Return dict in format = {
            "items":[{Events}], 
            "total": int, 
            "page": int, 
            "size": int, 
            "pages": int
            }"""
        result = jsonable_encoder(paginate(super().get_all(db), params))
        result['items'] = self.sort_events(result['items'])
        return result

    def get(self, db: Session, id: int):
        result = jsonable_encoder(super().get(db, id))
        return self.sort_events(result)

    
    def update(self, db: Session, id: int, event: EventSchema) -> None:
        if not super().get(db, id):
            raise HTTPException(status_code=404, detail="Not Found")
        self._check_exist_or_create_sensor(db, sensor_id=event.sensor_id)
        super().update(db, id, event)

    def get_by_sensor_id(self, db: Session, sensor_id: int) -> list[Event]:
        """Return event by sensor id"""
        return db.query(self.model).filter(self.model.sensor_id == sensor_id).all()
    
    def get_events_filter(self, db: Session, event_filter: EventFilter) -> list:
        """Return filtered events"""
        query_filter = event_filter.filter(select(Event))
        return db.execute(query_filter).scalars().all()


    def _check_exist_or_create_sensor(self, db: Session, sensor_id: int) -> None:
        """Function will check if the sensor exists, if not, it will create it"""
        if not sensors_service.get(db, sensor_id):
            sensors_service.create(db, SensorSchema(id=sensor_id))

    def sort_events(self, events: list) -> list[dict]:
        """
        Retuen list of events in format {
            id,
            name,
            temperature,
            humidity
        }
        """
        result = None
        if type(events) == dict:
            event = events
            result = {
                'id': event['id'],
                "sensor_id": event['sensor_id'],
                'name': event['name'],
                'temperature': event['temperature'],
                'humidity': event['humidity']
            }
        else:
            result = []
            for event in events:
                result.append({
                    'id': event['id'],
                    "sensor_id": event['sensor_id'],
                    'name': event['name'],
                    'temperature': event['temperature'],
                    'humidity': event['humidity']
                })
        return result


event_service = EventServise(Event)
