from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine 
from fastapi import Depends
from ignore import Gitignore

class database:

    engine = create_engine(Gitignore.DATABASE_URL, echo=True) #echo=true mostra no terminal os comandos sql que serão enviados

    def create_db_and_tables():
        SQLModel.metadata.create_all(database.engine)

    def get_session():
        with Session(database.engine) as session:
            yield session

    SessionDep = Annotated[Session, Depends(get_session)]