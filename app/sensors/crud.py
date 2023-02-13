from sqlalchemy.orm import Session
from fastapi_pagination import Params, paginate

from app.sensors.schema import RequestSensor, SensorSchema
from app.db.models import Sensor
from app.sensors.utils import parse_sensors
from app.crud_base import BaseCRUD

class SensorCRUD(BaseCRUD[Sensor]):

    def get_all(self, db: Session, params: Params):
        return paginate(super().get_all(db), params)
    
    def create_multi(self, db: Session, objs: RequestSensor):
        return super().create_multi(db, objs.sensors)


sensors = SensorCRUD(Sensor)

# def create_sensors_by_list(db: Session, import_sensors: RequestSensor):
#     for sensor in import_sensors.sensors:
#         create_sensor(db, Sensor(name=sensor.name, type=sensor.type))
#     return sensor


# def create_sensor(db: Session, sensor: Sensor):
#     db.add(sensor)
#     db.commit()


# def get_sensor_by_id(db: Session, sensor_id: int):
#     return db.query(Sensor).filter(Sensor.id == sensor_id).first()


# def get_all_sensors(db: Session, params: Params):
#     return paginate(parse_sensors(db), params)


# def update_sensors(db: Session, id: int, sensor: SensorSchema):
#     db.query(Sensor).filter(Sensor.id == id).update({
#         'name': sensor.name,
#         'type': sensor.type
#         })
#     db.commit()
#     return sensor


# def delete_sensor(db: Session, id: int):
#     sensor = get_sensor_by_id(db, id)
#     db.delete(sensor)
#     db.commit()