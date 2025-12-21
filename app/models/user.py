from typing import List
from pydantic import EmailStr
from uuid import UUID, uuid4
from sqlmodel import Relationship, SQLModel, Field

class UserInDB(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    email: EmailStr = Field(index=True)
    password: str
    patrimony: float = Field(default=0.0)
    disabled: bool = Field(default=False)
    historic: List["OperationInDB"] = Relationship(back_populates="user") # type: ignore #estabelecendo uma conexão
    bought: List["Shopping"] = Relationship(back_populates="user") # type: ignore