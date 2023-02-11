from pydantic import BaseModel
from typing import Optional


class SensorForm(BaseModel):
    name: Optional[str] = None
    type: int


class RequestSensor(BaseModel):
    sensors: list[SensorForm]