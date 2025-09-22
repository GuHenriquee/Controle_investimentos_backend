from objects import UserCreate, UserInDB, Operation, OperationResponse, UserResponse, Login, Token
from operations import Operations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from database import database
from contextlib import asynccontextmanager
from ignore import Gitignore
from sqlmodel import select
from login import LoginAndJWT


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)



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
        password= LoginAndJWT.hashing_password(user.password),  
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    print("Usuário para 'salvar' no banco de dados:", db_user)

    return db_user


@app.post("/api/login/", status_code=200)
def isLoged(loginCredentiasl: Login, session: database.SessionDep)-> Token:

    queryEmail = select(UserInDB).where(UserInDB.email == loginCredentiasl.email)
    existingUser = session.exec(queryEmail).first()
    
    if not existingUser or not LoginAndJWT.verify_password(loginCredentiasl.password, existingUser.password):
        raise HTTPException(status_code=401, detail="incorrect Email or password")
    
    access_token = LoginAndJWT.create_access_token(data={"sub": existingUser.email}) #"sub" abreviação de "Subject"(Sujeito). É a "reivindicação" (claim) que identifica sobre quem é o token. Em um sistema de login, o "sujeito" é o usuário.

    return Token(access_token=access_token, token_type="bearer")  #bearer token funciona como dinheiro ou um ingresso de show: qualquer pessoa que o porta (que o possui) tem o direito de usá-lo. O sistema de segurança não precisa de mais nenhuma prova, ele apenas verifica se o token em si é válido.


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




    