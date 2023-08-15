from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:qwerty@34.100.218.48/HealthManagement"
print("This package called")
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind = engine)
