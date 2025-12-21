from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine 
from fastapi import Depends
from core.config import settings
class database:

    engine = create_engine(settings.DATABASE_URL, echo=True) 

    @staticmethod
    def create_db_and_tables():
        SQLModel.metadata.create_all(database.engine)

    @staticmethod
    def get_session():
        with Session(database.engine) as session:
            yield session
    
    @staticmethod
    def SessionLocal() -> Session:
        return Session(database.engine)


_SessionDep = Annotated[Session, Depends(database.get_session)]

database.SessionDep = _SessionDep