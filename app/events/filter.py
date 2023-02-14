from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional
from pydantic import Field
from app.db.models import Event


class EventFilter(Filter):
    temperature__gte: Optional[float] = Field(default=0,
        ge=0,
        le=100,
        alias="temperature",
        description="Return events whose temperature >= given",
        )
    
    humidity__gte: Optional[float] = Field(default=0,
        ge=0,
        le=100,
        alias="humidity",
        description="Return events whose humidity >= given",
       )

    class Constants(Filter.Constants):
        model = Event
    
    class Config:
        allow_population_by_field_name = True