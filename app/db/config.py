from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import DATABASE_URL


engine = create_engine(DATABASE_URL)
Session = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()