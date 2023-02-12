from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Params

from app.utils import get_db
from .schema import RequestEvent, EventSchema, ResponseSchema
import app.events.crud as crud


router = APIRouter()


@router.post("", name='', response_model=ResponseSchema)
async def create_event(request: RequestEvent, db: Session=Depends(get_db)):
    crud.create_event(db, request)
    return ResponseSchema(detail="Successfully created data")


@router.get("", name='', response_model=ResponseSchema)
async def get_all_events(params: Params = Depends(), db: Session=Depends(get_db)):
    result = crud.get_all_events(db, params)
    return ResponseSchema(detail="Successfully fetch events", result=result)


@router.get("/{id}", name='', response_model=ResponseSchema)
async def get_event_by_id(id: int, db: Session=Depends(get_db)):
    result = crud.get_event_by_id(db, id)
    return ResponseSchema(detail="Successfully fetch event data by id", result=result)


@router.put("/{id}", name='', response_model=ResponseSchema)
async def update_event(id:int, request: EventSchema, db: Session=Depends(get_db)):
    crud.updare_event(db, id, request)
    return ResponseSchema(detail="Successfully updated data")


@router.delete("/{id}", name='', response_model=ResponseSchema)
async def delete_event(id: int, db: Session=Depends(get_db)):
    crud.delete_event(db, id)
    return ResponseSchema(detail="Successfully deleted data")
