from typing import List
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from sqlmodel import Relationship, SQLModel, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class Token (BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Login(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    patrimony: float

class UserInDB(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    email: EmailStr = Field(index=True)
    password: str
    patrimony: float = Field(default=0.0)
    disabled: bool = Field(default=False)
    historic: List["OperationInDB"] = Relationship(back_populates="user") # type: ignore #estabelecendo uma conexão
    bought: List["Shopping"] = Relationship(back_populates="user") # type: ignore