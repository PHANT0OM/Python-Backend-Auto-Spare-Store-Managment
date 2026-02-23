from sqlmodel import SQLModel, create_engine, Session
from config import settings

engine = create_engine(settings.DATABASE_URL, echo=(settings.ENVIRONMENT != "production"))

def create_database_and_tables():
    SQLModel.metadata.create_all(engine)
    
def Get_Session():
    with Session(engine) as session:
        yield session