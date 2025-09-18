from typing import List, Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from sqlmodel import Relationship, SQLModel, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class Operation(BaseModel):
    amount: float
    operationType: str
    previousValue: float 

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

class UserInDB(SQLModel, table=True):
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    email: EmailStr = Field(index=True)
    password: str
    patrimony: float = Field(default=0.0)
    historic: List["OperationInDB"] = Relationship(back_populates="user") #estabelecendo uma conexão

# Modelo SÓ PARA A RESPOSTA, sem a senha
class UserResponse(BaseModel):
    name: str
    email: EmailStr
    patrimony: float

