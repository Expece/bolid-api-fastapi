from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils import get_db
from .forms import RequestSensor, SensorForm
import app.sensors.crud as crud

router = APIRouter()


@router.post('/post', name='')
async def create_sensor(request: RequestSensor, db: Session = Depends(get_db)):
    sensor = crud.create_sensors_by_list(db, request)
    return sensor


@router.get('/get', name='')
async def get_sensors(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    sensors = crud.get_sensors(db, skip, limit)
    return sensors


@router.get('/get/{id}', name='')
async def get_sensor_by_id(id: int, db: Session = Depends(get_db)):
    sensor = crud.get_sensor_by_id(db, id)
    return sensor


@router.put('/update/{id}', name='')
async def update_sensor(id:int, request: SensorForm, db: Session = Depends(get_db)):
    sensors = crud.update_sensors(db, id, request)
    return sensors


@router.delete('/delete/{id}', name='')
async def delete_sensor(id: int, db: Session = Depends(get_db)):
    crud.delete_sensor(db, id)
    return HTTPException(status_code=200)
