from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Params
from fastapi import HTTPException

from app.utils import get_db
from app.sensors.schema import RequestSensor, SensorSchema, ResponseSchema, UpdateSensorSchema
from app.sensors.sensor_service import sensors_service


router = APIRouter()


@router.post("", name='create sensor', response_model=ResponseSchema)
async def create_sensor(new_sensor: SensorSchema, db: Session = Depends(get_db)):
    """Create sensor"""
    sensors_service.create(db, new_sensor)
    return ResponseSchema(detail="Successfully created data")


@router.post("/multi", name='create sensors', response_model=ResponseSchema)
async def create_multi_sensors(request: RequestSensor, db: Session = Depends(get_db)):
    """Create multi sensors. Input to "sensors" list of data"""
    sensors_service.create_multi(db, request)
    return ResponseSchema(detail="Successfully created data")


@router.get("", name='get all sensors', response_model=ResponseSchema)
async def get_all_sensors(params: Params = Depends(), db: Session = Depends(get_db)):
    """Return all sensors broken down by pages. Sensors are sorted by id.
        - result: {
            - "items": [Sensors],
            - "total": int,
            - "page": int,
            - "size": int,
            - "pages": int
        - }"""
    result = sensors_service.get_all(db, params)
    if not result['items']:
        raise HTTPException(status_code=404, detail="Not Found")
    return ResponseSchema(detail="Successfully fetch sensors data", result=result)


@router.get("/{id}", name='get sensor by id', response_model=ResponseSchema)
async def get_sensor_by_id(id: int, db: Session = Depends(get_db)):
    """Return sensor by id"""
    result = sensors_service.get(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return ResponseSchema(detail="Successfully fetch sensor data by id", result=result)


@router.put("/{id}", name='update sensor by id', response_model=ResponseSchema)
async def update_sensor(id:int, updated_sensor: UpdateSensorSchema, db: Session = Depends(get_db)):
    """Update sensor by id"""
    sensors_service.update(db, id, updated_sensor)
    return ResponseSchema(detail="Successfully updated data")


@router.delete("/{id}", name='delete sensor by id', response_model=ResponseSchema)
async def delete_sensor(id: int, db: Session = Depends(get_db)):
    """Delete sensor by id"""
    sensors_service.delete(db, id)
    return ResponseSchema(detail="Successfully deleted data")

