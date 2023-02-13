from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import TypeVar, Any, Type, Generic
from pydantic import BaseModel



ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
CreateMultiSchematype = TypeVar('CreateMultiSchematype', bound=BaseModel)

class BaseCRUD(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    
    def create(self, db: Session, obj: CreateSchemaType):
        obj_data = jsonable_encoder(obj)
        db.add(self.model(**obj_data))
        db.commit()
        return obj_data

    
    def create_multi(self, db: Session, objs: CreateMultiSchematype):
        result = []
        _objs = jsonable_encoder(objs)
        for obj in _objs:
            result.append(obj)
            db.add(self.model(**obj))
        db.commit
        return result
    
    
    def get(self, db: Session, id: Any) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()
    

    def get_all(self, db: Session, offset: int=0, limit: int=100) -> list[ModelType]:
        return db.query(self.model).offset(offset).limit(limit).all()


    def update(self, db: Session, id: Any, obj: UpdateSchemaType):
        obj_data = jsonable_encoder(obj)
        db_obj = db.query(self.model).filter(self.model.id == id).first()

        db_obj = self._set_new_atr(db_obj, obj, obj_data)
        
        db.add(db_obj)
        db.commit()
        return self.get(db, id)


    def delete(self, db: Session, id: int):
        obj = self.get(db, id)
        db.delete(obj)
        db.commit
        return obj
    
    def _set_new_atr(self, db_obj: ModelType, obj: UpdateSchemaType, obj_data: Any):
        if isinstance(obj, dict):
            updated_obj = obj
        else:
            updated_obj = obj.dict(exclude_unset=True)
        
        for field in obj_data:
            setattr(db_obj, field, updated_obj[field])
        return db_obj