from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi.encoders import jsonable_encoder
from typing import TypeVar, Any, Type, Generic
from pydantic import BaseModel
from fastapi import HTTPException


ModelType = TypeVar('ModelType')
ModelSchemaType = TypeVar('ModelSchemaType', bound=BaseModel)



class BaseCRUD(Generic[ModelType]):
    """Base class in which CRUD operations are implemented"""

    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    
    def create(self, db: Session, obj: ModelSchemaType) -> None:
        """Create object"""
        obj_data = jsonable_encoder(obj)
        db.add(self.model(**obj_data))
        db.commit()
    
    def create_multi(self, db: Session, objs: ModelSchemaType) -> None:
        """Create multi objects"""
        for obj in objs:
            self.create(db, obj)
    
    
    def get(self, db: Session, id: Any) -> ModelType | None:
        """Return object from database by id"""
        obj = db.query(self.model).filter(self.model.id == id).first()
        return obj
    

    def get_all(self, db: Session) -> list[ModelType]:
        """Retunrb all objects from database"""
        objs = db.query(self.model).order_by(self.model.id, self.model.name).all()
        return objs


    def update(self, db: Session, id: Any, obj: ModelSchemaType):
        obj_data = jsonable_encoder(obj)
        db_obj = db.query(self.model).filter(self.model.id == id).first()

        db_obj = self._set_new_atr(db_obj, obj, obj_data)
        
        db.add(db_obj)
        db.commit()


    def delete(self, db: Session, id: int):
        obj = db.query(self.model).filter(self.model.id == id).first()
        db.delete(obj)
        db.commit
    
    def _set_new_atr(self, db_obj: ModelType, obj: ModelSchemaType, obj_data: Any):
        if isinstance(obj, dict):
            updated_obj = obj
        else:
            updated_obj = obj.dict(exclude_unset=True)
        
        for field in obj_data:
            setattr(db_obj, field, updated_obj[field])
        return db_obj
    
    def _get_last_id(self, db: Session):
        return db.query(self.model).order_by(desc(self.model.id)).first().id
    
    
        