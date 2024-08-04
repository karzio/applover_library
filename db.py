from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432")
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

