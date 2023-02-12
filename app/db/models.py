from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from app.db.config import Base
import enum


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    name = Column(String, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)


class Sensor(Base):
    __tablename__ = 'sensor'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    type = Column(Integer, default=1)
