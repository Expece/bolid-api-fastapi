from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import TypeVar, Any, Type, Generic
from pydantic import BaseModel
from fastapi import HTTPException


ModelType = TypeVar('ModelType')
ModelSchemaType = TypeVar('ModelSchemaType', bound=BaseModel)



class BaseCRUD(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    
    def create(self, db: Session, obj: ModelSchemaType):
        obj_data = jsonable_encoder(obj)
        db.add(self.model(**obj_data))
        db.commit()

    
    def create_multi(self, db: Session, objs: ModelSchemaType):
        _objs = jsonable_encoder(objs)
        for obj in _objs:
            db.add(self.model(**obj))
        db.commit
    
    
    def get(self, db: Session, id: Any) -> ModelType | None:
        obj = db.query(self.model).filter(self.model.id == id).one_or_none()
        return obj
    

    def get_all(self, db: Session, offset: int=0, limit: int=100) -> list[ModelType]:
        objs = db.query(self.model).offset(offset).limit(limit).all()
        return objs


    def update(self, db: Session, id: Any, obj: ModelSchemaType):
        obj_data = jsonable_encoder(obj)
        db_obj = self.get(db, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Not Found")

        db_obj = self._set_new_atr(db_obj, obj, obj_data)
        
        db.add(db_obj)
        db.commit()


    def delete(self, db: Session, id: int):
        obj = self.get(db, id)
        db.delete(obj)
        db.commit
    
    
    def _set_new_atr(self, db_obj: ModelType, obj: ModelSchemaType, obj_data: Any) -> ModelType:
        if isinstance(obj, dict):
            updated_obj = obj
        else:
            updated_obj = obj.dict(exclude_unset=True)
        
        for field in obj_data:
            setattr(db_obj, field, updated_obj[field])
        return db_obj
    
        