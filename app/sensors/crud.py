from sqlalchemy.orm import Session
from fastapi import HTTPException

from .forms import RequestSensor, SensorForm
from app.db.models import Sensor

# from app.sensors.validations import check_sensor_type


def create_sensors_by_list(db: Session, import_sensors: RequestSensor):
    for sensor in import_sensors.sensors:
        create_sensor(db, Sensor(name=sensor.name, type=sensor.type))
    return sensor


def create_sensor(db: Session, sensor: Sensor):
    db.add(sensor)
    db.commit()


def get_sensor_by_id(db: Session, sensor_id: int):
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


def get_sensors(db: Session, skip: int, limit: int):
    return db.query(Sensor).offset(skip).limit(limit).all()


def update_sensors(db: Session, id: int, sensor: SensorForm):
    db.query(Sensor).filter(Sensor.id == id).update({
        'name': sensor.name,
        'type': sensor.type
        })
    db.commit()
    return sensor


def delete_sensor(db: Session, id: int):
    sensor = get_sensor_by_id(db, id)
    db.delete(sensor)
    db.commit()