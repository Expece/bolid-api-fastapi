from pydantic import BaseModel, validator
from typing import Optional, TypeVar
from fastapi import HTTPException


T = TypeVar('T')


class SensorInDB(BaseModel):
    id: int
    name: Optional[str] = None
    type: int


class SensorSchema(BaseModel):
    name: Optional[str] = None
    type: int

    @validator('type', pre=True)
    def type_validator(cls, sensor_type):
        types = [1, 2, 3]
        if not sensor_type:
            raise HTTPException(status_code=400, detail="Sensor type can be between 1 and 3")
        if type(sensor_type) != int:
            raise HTTPException(status_code=400, detail="Value of sensor type must be integer")
        if sensor_type not in types:
            raise HTTPException(status_code=400, detail="Sensor type can be between 1 and 3")
        return sensor_type

class RequestSensor(BaseModel):
    sensors: list[SensorSchema]

class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None