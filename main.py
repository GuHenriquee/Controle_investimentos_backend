from objects import UserCreate, UserInDB, Operation, OperationResponse
from operations import Operations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from database import database
from contextlib import asynccontextmanager

app = FastAPI()


# 1. Adicione o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], # A origem completa do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 2. Adicione o middleware de segurança de Host, só requests vindas desse lugar podem ser usadas
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1"] # 127.0.0.1 e localhost são a mesma coisa
)

# Adicione o 'response_model' para filtrar a resposta
@app.post("/api/register/") 
def create_user(user: UserCreate, session: database.SessionDep)-> UserInDB:

    final_user_data = {
        "id": uuid4(),
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "patrimony": 0.0,
        "historic": []
    }
    session.add(final_user_data)
    session.commit()
    session.refresh(final_user_data)
    
    print("Usuário para 'salvar' no banco de dados:", final_user_data)

    return final_user_data


@app.post("/api/operation/", response_model=OperationResponse)
def operator(operation: Operation):

    lastOperation = {
        "amount":operation.amount,
        "operationType": operation.operationType,
        "previousValue": operation.previousValue,
        "newValue": 0
    }

    if (lastOperation):
        if (lastOperation['operationType'] == "Retirar"):
            lastOperation['newValue'] = Operations.minus( lastOperation['previousValue'], lastOperation['amount'])
        else:
            lastOperation['newValue'] = Operations.sum( lastOperation['previousValue'], lastOperation['amount'])
    

    return lastOperation




    