from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def create_database_and_tables():
    SQLModel.metadata.create_all(engine)
    
def Get_Session():
    with Session(engine) as session:
        yield session

    