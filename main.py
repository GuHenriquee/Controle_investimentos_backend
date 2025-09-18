from objects import UserCreate, UserInDB, Operation, OperationResponse, UserResponse
from operations import Operations
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from database import database
from contextlib import asynccontextmanager
from ignore import Gitignore
from passlib.context import CryptContext
from sqlmodel import select




@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
#"deprecated="auto"" fará com que senhas com hashes antigos sejam atualizadas automaticamente na próxima vez que o usuário fizer login.

def hashing_password(password: str) -> str:
    return pwd_context.hash(password)


# 1. Adicione o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Gitignore.FRONT_URL], # A origem completa do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 2. Adicione o middleware de segurança de Host, só requests vindas desse lugar podem ser usadas
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1"] # 127.0.0.1 e localhost são a mesma coisa
)


@app.post("/api/register/", status_code=201) #201 = created
def create_user(user: UserCreate, session: database.SessionDep)-> UserResponse:

    query = select(UserInDB).where(UserInDB.email == user.email) #criando consulta
    existing_user = session.exec(query).first()                  #executando consulta

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserInDB(
        name=user.name,
        email=user.email,
        password= hashing_password(user.password),  
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    print("Usuário para 'salvar' no banco de dados:", db_user)

    return db_user


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




    