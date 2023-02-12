from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Params

from app.utils import get_db
from app.sensors.schema import RequestSensor, SensorSchema, ResponseSchema
import app.sensors.crud as crud


router = APIRouter()


@router.post("", name='', response_model=ResponseSchema)
async def create_sensor(sensors_request: RequestSensor, db: Session = Depends(get_db)):
    crud.create_sensors_by_list(db, sensors_request)
    return ResponseSchema(detail="Successfully created data")


@router.get("", name='', response_model=ResponseSchema)
async def get_all_sensors(params: Params = Depends(), db: Session = Depends(get_db)):
    result = crud.get_all_sensors(db, params)
    return ResponseSchema(detail="Successfully fetch sensors data", result=result)


@router.get("/{id}", name='', response_model=ResponseSchema)
async def get_sensor_by_id(id: int, db: Session = Depends(get_db)):
    result = crud.get_sensor_by_id(db, id)
    return ResponseSchema(detail="Successfully fetch sensor data by id", result=result)


@router.put("{id}", name='', response_model=ResponseSchema)
async def update_sensor(id:int, updated_sensor: SensorSchema, db: Session = Depends(get_db)):
    crud.update_sensors(db, id, updated_sensor)
    return ResponseSchema(detail="Successfully updated data")


@router.delete("{id}", name='', response_model=ResponseSchema)
async def delete_sensor(id: int, db: Session = Depends(get_db)):
    crud.delete_sensor(db, id)
    return ResponseSchema(detail="Successfully deleted data")

