from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Params
from fastapi import HTTPException
from fastapi_filter import FilterDepends

from app.utils import get_db
from .schema import RequestEvents, EventSchema, ResponseSchema
from app.events.event_servise import event_service
from app.events.filter import EventFilter

router = APIRouter()


@router.post("", name='create event', response_model=ResponseSchema)
async def create_event(request: EventSchema, db: Session=Depends(get_db)):
    """Create event"""
    result = event_service.create(db, request)
    return ResponseSchema(detail="Successfully created event", result=result)


@router.post("/multi", name='create multi events', response_model=ResponseSchema)
async def create_multi_events(request: RequestEvents, db: Session=Depends(get_db)):
    """Create multi events"""
    event_service.create_multi(db, request)
    return ResponseSchema(detail="Successfully created multi of event")


@router.get("", name='get all events', response_model=ResponseSchema)
async def get_all_events(params: Params = Depends(), db: Session=Depends(get_db)):
    """Return all events broken down by pages"""
    result = event_service.get_all(db, params)
    if not result['items']:
        raise HTTPException(status_code=404, detail="Not Found")
    return ResponseSchema(detail="Successfully fetch events", result=result)


@router.get("/{id}", name='get event by id', response_model=ResponseSchema)
async def get_event_by_id(id: int, db: Session=Depends(get_db)):
    """Return event by id"""
    result = event_service.get(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return ResponseSchema(detail="Successfully fetch event by id", result=result)


@router.put("/{id}", name='update event by id', response_model=ResponseSchema)
async def update_event(id:int, request: EventSchema, db: Session=Depends(get_db)):
    """Update event by id"""
    event_service.update(db, id, request)
    return ResponseSchema(detail="Successfully updated event")


@router.delete("/{id}", name='delete event by id', response_model=ResponseSchema)
async def delete_event(id: int, db: Session=Depends(get_db)):
    """Delete event by id"""
    event_service.delete(db, id)
    return ResponseSchema(detail="Successfully deleted event")


@router.get("/by-sensor-id/{sensor_id}", name='get events by sensor id', response_model=ResponseSchema)
async def get_events_by_sensor_id(sensor_id: int, db: Session = Depends(get_db)):
    """Return all events by entered sensor_id"""
    result = event_service.get_by_sensor_id(db, sensor_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return ResponseSchema(detail="Successfully fetch events by sensor id", result=result)


@router.get("/filter-by/", name='get filtered events') #, response_model=ResponseSchema)
async def get_filtered_events(event_filter: EventFilter = FilterDepends(EventFilter),  db: Session = Depends(get_db)):
    """Return filtered events"""
    result = event_service.get_events_filter(db, event_filter)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return ResponseSchema(detail="Successfully fetch events by sensor id", result=result)