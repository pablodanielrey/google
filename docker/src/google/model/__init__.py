import os
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base

engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
    os.environ['GOOGLE_DB_USER'],
    os.environ['GOOGLE_DB_PASSWORD'],
    os.environ['GOOGLE_DB_HOST'],
    os.environ['GOOGLE_DB_NAME']
), echo=True)
Session = sessionmaker(bind=engine)

from .GoogleModel import GoogleModel

__all__ = [
    'GoogleModel'
]

from .entities import *

def crear_schema():
    Base.metadata.create_all(engine)
