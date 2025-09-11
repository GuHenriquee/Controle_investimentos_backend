from typing import List, Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID 

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

class UserInDB(BaseModel): 
    id: UUID 
    name: str
    email: EmailStr
    password: str
    patrimony: float
    historic: Optional[List[Operation]] = None 

# Modelo SÓ PARA A RESPOSTA, sem a senha
class UserResponse(BaseModel):
    name: str
    email: EmailStr
    patrimony: float