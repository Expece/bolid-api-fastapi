from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.config import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    name = Column(String, nullable=False)
    temperature = Column(Integer)
    humidity = Column(Integer)


class Strange_event(Base):
    __tablename__ = 'strange_events'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    name = Column(String, nullable=False)
    temperature = Column(Integer)
    humidity = Column(Integer)


class Sensor(Base):
    __tablename__ = 'sensor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(Integer)
