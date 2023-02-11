from pydantic import BaseModel
from typing import Optional


class EventForm(BaseModel):
    sensor_id: int
    name: str
    temperature: Optional[int] = None
    humidity: Optional[int] = None


class StrangeEventForm(BaseModel):
    sensor_id: int
    name: str
    temperature: Optional[int] = None
    humidity: Optional[int] = None


class RequestEvents(BaseModel):
    events: list[EventForm]