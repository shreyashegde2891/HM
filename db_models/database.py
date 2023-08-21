from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:qwerty@pruinhlth-nprd-dev-scxlyx-7250:asia-south1:sahi-dev/HealthManagement"
print("This package called")
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind = engine)
