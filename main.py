from objects import UserCreate, UserResponse, Operation, OperationResponse
from operations import Operations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from fastapi.middleware.trustedhost import TrustedHostMiddleware

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
@app.post("/api/register/", response_model=UserResponse) 
def registerUser(user: UserCreate):

    final_user_data = {
        "id": uuid4(),
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "patrimony": 0.0,
        "historic": []
    }
    
    print("Usuário para 'salvar' no banco de dados:", final_user_data)

    return final_user_data


@app.post("/api/operation/", response_model=OperationResponse)
def operator(operation: Operation):

    lastOperation = {
        "transactionType": operation.operationType,
        "amount":operation.amount,
        "previousValue": operation.previousValue,
        "newValue": 0
    }

    if (lastOperation['transactionType'] == "Retirar"):
        lastOperation['newValue'] = Operations.minus( lastOperation['previousValue'], lastOperation['amount'])
    else:
        lastOperation['newValue'] = Operations.sum( lastOperation['previousValue'], lastOperation['amount'])
    

    return lastOperation




    