from fastapi import FastAPI

from app.db.config import engine
import app.db.models as models
from app.settings import PROJECT_NAME, VERSION
from app.events.handlers import router as events_router
from app.sensors.handlers import router as sensors_router


models.Base.metadata.create_all(engine)

app = FastAPI(title=PROJECT_NAME,
            version=VERSION)

app.include_router(events_router, prefix='/events', tags=["Events"])
app.include_router(sensors_router, prefix='/sensors', tags=["Sensors"])