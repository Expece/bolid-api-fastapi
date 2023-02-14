from .schema import RequestEvents, EventSchema
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Params
from fastapi.encoders import jsonable_encoder
from typing import Iterable
from sqlalchemy.sql.expression import select

from app.db.models import Event, Sensor
from app.crud_base import BaseCRUD
from app.events.filter import EventFilter
from app.sensors.sensor_service import sensors_service


class EventServise(BaseCRUD[Event]):
    """Class for interacting with an Event table in a database"""

    def create(self, db: Session, event: EventSchema) -> None:
        """Create event. If there is no sensor
         associated with the event creates it"""
        self._check_exist_or_create_sensor(db, event.sensor_id)
        _event = jsonable_encoder(event)
        db.add(self.model(**_event))
        db.commit()

    
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
        return jsonable_encoder(paginate(super().get_all(db), params))


    def get_by_sensor_id(self, db: Session, sensor_id: int) -> list[Event] | list:
        """Return sensor by id"""
        return db.query(self.model).filter(self.model.sensor_id == sensor_id).all()
        
    
    def get_events_filter(self, db: Session, event_filter: EventFilter) -> list:
        """Return filtered events"""
        query_filter = event_filter.filter(select(Event))
        return db.execute(query_filter).scalars().all()


    def _check_exist_or_create_sensor(self, db: Session, sensor_id: int) -> None:
        """Function will check if the sensor exists, if not, it will create it"""
        if not sensors_service.get(db, sensor_id):
            sensors_service.create(db, sensor=Sensor(id=sensor_id, name=None))

event_service = EventServise(Event)
