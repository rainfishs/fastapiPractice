from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)


# Define Tables(Models)
Base = declarative_base()

# factory method
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
