from typing import List, Optional
from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID 

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class Historical(BaseModel):
    amount: float
    transactionType: str
    previousValue: float 

class UserInDB(BaseModel): 
    id: UUID 
    name: str
    email: EmailStr
    password: str
    patrimony: float
    historic: Optional[List[Historical]] = None 

# Modelo SÓ PARA A RESPOSTA, sem a senha
class UserResponse(BaseModel):
    name: str
    email: EmailStr
    patrimony: float