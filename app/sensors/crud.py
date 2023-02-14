from sqlalchemy.orm import Session
from fastapi_pagination import Params, paginate
from fastapi.encoders import jsonable_encoder
from typing import Any

from app.sensors.schema import RequestSensor, SensorSchema
from app.db.models import Sensor
from app.crud_base import BaseCRUD

class SensorCRUD(BaseCRUD[Sensor]):

    def get_all(self, db: Session, params: Params) -> Any:
        return jsonable_encoder(paginate(super().get_all(db), params))
    
    def create_multi(self, db: Session, objs: RequestSensor):
        super().create_multi(db, objs.sensors)


sensors = SensorCRUD(Sensor)
