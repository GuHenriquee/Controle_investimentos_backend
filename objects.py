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


# Modelo SÓ PARA A RESPOSTA, sem a senha
class UserResponse(BaseModel):
    name: str
    email: EmailStr
    patrimony: float

