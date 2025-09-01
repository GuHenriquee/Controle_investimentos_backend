from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI
from uuid import uuid4

app = FastAPI() # Este é o seu objeto principal, o "cérebro" da sua API. Tudo se conecta a ele.

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Historical(BaseModel):
    amount:float
    transactionType:str
    previusValue:float

class FinalUser(BaseModel):
    id: int
    name: str
    email: str
    password: str
    patrimony: float
    historic: Optional[List[Historical]] = None 


@app.post("/api/register") 
def registerUser(user: UserCreate):

    final_user_data = {
        "id": uuid4(),
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "patrimony": 0.0,
        "historic": [] # Um histórico vazio é melhor que 'None'
    }
    print("Usuário para 'salvar' no banco de dados:", final_user_data)

    return finalUser