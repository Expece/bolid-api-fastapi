from .schema import RequestEvents, EventSchema
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Params
from fastapi.encoders import jsonable_encoder
from typing import Any
from sqlalchemy.sql.expression import select

from app.db.models import Event, Sensor
from app.crud_base import BaseCRUD
from app.sensors.crud import sensors
from app.events.filter import EventFilter



class EventServise(BaseCRUD[Event]):

    def create(self, db: Session, event: EventSchema):
        self._check_exist_or_create_sensor(db, event.sensor_id)
        _event = jsonable_encoder(event)
        db.add(self.model(**_event))
        db.commit()

    
    def create_multi(self, db: Session, events: RequestEvents):
        for event in events.events:
            self._check_exist_or_create_sensor(db, event.sensor_id)
            _event = jsonable_encoder(event)
            db.add(self.model(**_event))
        db.commit()
    

    def get_all(self, db: Session, params: Params) -> Any:
        return jsonable_encoder(paginate(super().get_all(db), params))


    def get_by_sensor_id(self, db: Session, sensor_id: int) -> list[Event] | list:
        return db.query(self.model).filter(self.model.sensor_id == sensor_id).all()
        
    
    def get_events_filter(self, db: Session, event_filter: EventFilter) -> list:
        query_filter = event_filter.filter(select(Event))
        return db.execute(query_filter).scalars().all()


    def _check_exist_or_create_sensor(self, db: Session, sensor_id: int):
        if not sensors.get(db, sensor_id):
            sensors.create(db, sensor=Sensor(id=sensor_id, name=None))

event_service = EventServise(Event)
