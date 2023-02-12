from pydantic import BaseModel, validator
from typing import Optional, TypeVar
from fastapi import HTTPException


T = TypeVar('T')


class EventInDB(BaseModel):
    id: int
    sensor_id: int
    name: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None


class EventSchema(BaseModel):
    sensor_id: int
    name: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None

    @validator('sensor_id', pre=True)
    def sensor_id_validator(cls, sensor_id):
        if not sensor_id:
            raise HTTPException(status_code=400, detail="The event must refer to the sensor")
        if type(sensor_id) != int:
            raise HTTPException(status_code=400, detail="Value of sensor id must be integer")
        return sensor_id

    
    @validator('name', pre=True)
    def event_name_validator(cls, name):
        if not name:
            raise HTTPException(status_code=400, detail="The event must have name")
        return name
    

    @validator('temperature', pre=True)
    def temperature_validator(cls, temperature):
        if type(temperature) != int and type(temperature) != float:
            raise HTTPException(status_code=400,
            detail="Temperature value mast be a number")
        return temperature


    @validator('humidity', pre=True)
    def humidity_validator(cls, humidity):
        if type(humidity) != int and type(humidity) != float:
            raise HTTPException(status_code=400,
            detail="Humidity value mast be a number")
        if humidity < 0 or humidity > 100:
            raise HTTPException(status_code=400,
            detail="Humidity is measured as a percentage from 0 to 100")
        return humidity

class StrangeEventSchema(BaseModel):
    sensor_id: int
    name: str
    temperature: Optional[int] = None
    humidity: Optional[int] = None


class RequestEvent(BaseModel):
    events: list[EventSchema]


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None