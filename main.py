from pydantic import BaseModel, EmailStr
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4, UUID # MUDANÇA 1: Importe o tipo UUID

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- MODELOS DE DADOS ---

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class Historical(BaseModel):
    amount: float
    transactionType: str
    previousValue: float # MUDANÇA 2: Corrigido o nome do campo

class UserInDB(BaseModel): # Renomeado para maior clareza
    id: UUID # MUDANÇA 1: O tipo do id agora é UUID
    name: str
    email: EmailStr
    password: str
    patrimony: float
    historic: Optional[List[Historical]] = None 

# MUDANÇA 3: Crie um modelo SÓ PARA A RESPOSTA, sem a senha
class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    patrimony: float

# --- ENDPOINT ---

# MUDANÇA 3: Adicione o 'response_model' para filtrar a resposta
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

    # O FastAPI irá receber este dicionário completo, mas só enviará
    # para o frontend os campos definidos em UserResponse.
    return final_user_data