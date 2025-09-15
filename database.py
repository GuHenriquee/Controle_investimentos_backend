from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends

class database:
    DATABASE_URL = "postgresql://postgres:Gurudoamor17@localhost/Investiment_control"

    engine = create_engine(DATABASE_URL, echo=True) #echo=true mostra no terminal os comandos sql que serão enviados

    def create_db_and_tables():
        SQLModel.metadata.create_all(database.engine)

    def get_session():
        with Session(database.engine) as session:
            yield session

    SessionDep = Annotated[Session, Depends(get_session)]