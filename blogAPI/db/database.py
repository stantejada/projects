from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Database URL
SQLALCHEMY_DB_URL = "sqlite:///./blogApp.db"

#creating the engine
engine = create_engine(SQLALCHEMY_DB_URL, echo=True)

#creating sessionlocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#creating Base

Base = declarative_base()
