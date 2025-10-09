from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict 
from uuid import UUID, uuid4
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone


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

class Operation(BaseModel):
    amount: float
    operationType: str

class OperationResponse(BaseModel):
    amount: float
    operationType: str
    previousValue: float
    newValue: float 

class OperationInDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    operationType: str
    previousValue: float
    newValue: float
    user_id: Optional[UUID] = Field(default=None, foreign_key="userindb.id")
    user: Optional["UserInDB"] = Relationship(back_populates="historic") #estabelecendo uma conexão e não será uma tabela no DB

class shopsName(BaseModel):
    type: str
    name: str
    amount: float
    price: float

class Shopping(SQLModel,table =True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), nullable=False, index=True )
    type:str
    name: str
    dataPrice: float
    amount: float
    quantity: float
    user_id: Optional[UUID] = Field(default=None, foreign_key="userindb.id")
    user: Optional["UserInDB"] = Relationship(back_populates="bought") 

class ShoppingResponse(BaseModel):
        type:str
        name: str
        dataPrice: float
        amount: float
        quantity: float
        model_config = ConfigDict(from_attributes=True)


class UserInDB(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    email: EmailStr = Field(index=True)
    password: str
    patrimony: float = Field(default=0.0)
    disabled: bool = Field(default=False)
    historic: List["OperationInDB"] = Relationship(back_populates="user") #estabelecendo uma conexão
    bought: List["Shopping"] = Relationship(back_populates="user")



# Modelo SÓ PARA A RESPOSTA, sem a senha
class UserResponse(BaseModel):
    name: str
    email: EmailStr
    patrimony: float


