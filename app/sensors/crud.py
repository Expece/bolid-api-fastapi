from sqlalchemy.orm import Session
from fastapi_pagination import Params, paginate

from app.sensors.schema import RequestSensor, SensorSchema
from app.db.models import Sensor
from app.crud_base import BaseCRUD

class SensorCRUD(BaseCRUD[Sensor]):

    def get_all(self, db: Session, params: Params):
        return paginate(super().get_all(db), params)
    
    def create_multi(self, db: Session, objs: RequestSensor):
        return super().create_multi(db, objs.sensors)


sensors = SensorCRUD(Sensor)
