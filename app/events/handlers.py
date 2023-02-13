from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Params

from app.utils import get_db
from .schema import RequestEvents, EventSchema, ResponseSchema
from app.events.crud import events

router = APIRouter()


@router.post("", name='create event', response_model=ResponseSchema)
async def create_event(request: EventSchema, db: Session=Depends(get_db)):
    result = events.create(db, request)
    return ResponseSchema(detail="Successfully created event", result=result)


@router.post("/multi", name='create multi events', response_model=ResponseSchema)
async def create_multi_events(request: RequestEvents, db: Session=Depends(get_db)):
    result = events.create_multi(db, request)
    return ResponseSchema(detail="Successfully created multi of event", result=result)


@router.get("", name='get all events', response_model=ResponseSchema)
async def get_all_events(params: Params = Depends(), db: Session=Depends(get_db)):
    result = events.get_all(db, params)
    return ResponseSchema(detail="Successfully fetch events", result=result)


@router.get("/{id}", name='get event by id', response_model=ResponseSchema)
async def get_event_by_id(id: int, db: Session=Depends(get_db)):
    result = events.get(db, id)
    return ResponseSchema(detail="Successfully fetch event by id", result=result)


@router.put("/{id}", name='update event by id', response_model=ResponseSchema)
async def update_event(id:int, request: EventSchema, db: Session=Depends(get_db)):
    result = events.update(db, id, request)
    return ResponseSchema(detail="Successfully updated event", result=result)


@router.delete("/{id}", name='delete event by id', response_model=ResponseSchema)
async def delete_event(id: int, db: Session=Depends(get_db)):
    result = events.delete(db, id)
    return ResponseSchema(detail="Successfully deleted event", result=result)


@router.get("/by-sensor-id/{sensor_id}", name='get events by sensor id', response_model=ResponseSchema)
async def get_events_by_sensor_id(sensor_id: int, db: Session = Depends(get_db)):
    result = events.get_by_sensor_id(db, sensor_id)
    return ResponseSchema(detail="Successfully fetch events by sensor id", result=result)
