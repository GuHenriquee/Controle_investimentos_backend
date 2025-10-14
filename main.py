from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from routers import criptoData
from database import database
from contextlib import asynccontextmanager
from ignore import Gitignore
from routers import createUser, login, operation, stocks, crypto, shoping
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import update_criptos_db

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    print("Iniciando o servidor e o agendador de tarefas...")
    
    scheduler.add_job(update_criptos_db, 'interval', hours=24, id="update_assets_24h")  # Função 'update_criptos_db' sera executada a cada 24 horas

    scheduler.start()

    yield
    print("Desligando o agendador de tarefas...")
    scheduler.shutdown()
    
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

app.include_router(createUser.router)
app.include_router(login.router)
app.include_router(operation.router)
app.include_router(stocks.router)
app.include_router(crypto.router)
app.include_router(shoping.router)
app.include_router(criptoData.router)





    