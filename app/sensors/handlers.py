from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Params

from app.utils import get_db
from app.sensors.schema import RequestSensor, SensorSchema, ResponseSchema
from app.sensors.crud import sensors


router = APIRouter()


@router.post("", name='create sensor', response_model=ResponseSchema)
async def create_sensor(sensors_request: SensorSchema, db: Session = Depends(get_db)):
    result = sensors.create(db, sensors_request)
    return ResponseSchema(detail="Successfully created data", result=result)


@router.post("/multi", name='create sensor', response_model=ResponseSchema)
async def create_multi_sensors(sensors_request: RequestSensor, db: Session = Depends(get_db)):
    result = sensors.create_multi(db, sensors_request)
    return ResponseSchema(detail="Successfully created data", result=result)


@router.get("", name='get all sensors', response_model=ResponseSchema)
async def get_all_sensors(params: Params = Depends(), db: Session = Depends(get_db)):
    result = sensors.get_all(db, params)
    return ResponseSchema(detail="Successfully fetch sensors data", result=result)


@router.get("/{id}", name='get sensor by id', response_model=ResponseSchema)
async def get_sensor_by_id(id: int, db: Session = Depends(get_db)):
    result = sensors.get(db, id)
    return ResponseSchema(detail="Successfully fetch sensor data by id", result=result)


@router.put("{id}", name='update sensor by id', response_model=ResponseSchema)
async def update_sensor(id:int, updated_sensor: SensorSchema, db: Session = Depends(get_db)):
    result = sensors.update(db, id, updated_sensor)
    return ResponseSchema(detail="Successfully updated data", result=result)


@router.delete("{id}", name='delete sensor by id', response_model=ResponseSchema)
async def delete_sensor(id: int, db: Session = Depends(get_db)):
    result = sensors.delete(db, id)
    return ResponseSchema(detail="Successfully deleted data", result=result)

