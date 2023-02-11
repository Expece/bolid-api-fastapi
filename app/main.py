from fastapi import FastAPI
from app.db.config import engine
import app.db.models as models


models.Base.metadata.create_all(engine)
app = FastAPI()