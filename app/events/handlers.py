from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils import get_db
from .forms import RequestEvents, EventForm
import app.events.crud as crud


router = APIRouter()


@router.post('/post', name='')
async def create_event(request: RequestEvents, db: Session=Depends(get_db)):
    event = crud.create_event(db, request)
    return event


@router.get('/get', name='')
async def get_events(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    event = crud.get_events(db, skip, limit)
    return event


@router.get('/get/{id}', name='')
async def get_event_by_id(id: int, db: Session=Depends(get_db)):
    event = crud.get_event_by_id(db, id)
    return event


@router.put('/update/{id}', name='')
async def update_event(id:int, request: EventForm, db: Session=Depends(get_db)):
    event = crud.updare_event(db, id, request)
    return event


@router.delete('/delete/{id}', name='')
async def delete_event(id: int, db: Session=Depends(get_db)):
    crud.delete_event(db, id)
    return HTTPException(status_code=200)
