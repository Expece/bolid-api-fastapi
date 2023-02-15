from sqlalchemy.orm import Session
from fastapi_pagination import Params, paginate
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from app.sensors.schema import RequestSensor, SensorSchema
from app.db.models import Sensor
from app.crud_base import BaseCRUD

class SensorService(BaseCRUD[Sensor]):
    
    def create(self, db: Session, sensor: SensorSchema):
        if super().get(db, sensor.id):
            super().update(db, sensor.id, sensor)
        else:
            super().create(db, sensor)


    def get_all(self, db: Session, params: Params) -> dict:
        """Get all sensors. Return dict in format = {
        "items":[{Sensors}], 
        "total": int, 
        "page": int, 
        "size": int, 
        "pages": int
        }"""
        result = jsonable_encoder(paginate(super().get_all(db), params))
        result['items'] = self.sort_sensors(result['items'])
        return result
    

    def get(self, db: Session, id: int):
        result = jsonable_encoder(super().get(db, id))
        if not result:
            return None
        return self.sort_sensors(result)


    def create_multi(self, db: Session, objs: RequestSensor):
        """Create multi sensors."""
        super().create_multi(db, objs.sensors)
        return super().get_all(db)


    def sort_sensors(self, sensors: list | dict) -> list[dict]:
        """
        Retuen list of sensors in format {
            id,
            name,
            type
        }
        """
        result = None
        if type(sensors) == dict:
            sensor = sensors
            result = {
                'id': sensor['id'],
                'name': sensor['name'],
                'type': sensor['type'],
            }
        else:
            result = []
            for sensor in sensors:
                result.append({
                    'id': sensor['id'],
                    'name': sensor['name'],
                    'type': sensor['type'],
                })
        return result


sensors_service = SensorService(Sensor)
