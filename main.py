from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from funcionalities.OSINT.blogData import blog_catcher_worker
from routers.requests import createUser, login, operation, shoping
from routers.frontData import crypto, stocks
from routers.admin import criptoData, osintAnalises
from funcionalities.APIs.database import database 
from contextlib import asynccontextmanager
from ignore import Gitignore
from apscheduler.schedulers.background import BackgroundScheduler
from funcionalities.requestsFuncs.scheduler import update_criptos_db
from funcionalities.APIs.coingekoData import CoingekoFuncions
from sqlmodel import SQLModel 

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")


def create_db_and_tables():
    print("Iniciando criação de tabelas (se não existirem)...")
    SQLModel.metadata.create_all(database.engine) 
    print("Tabelas verificadas/criadas com sucesso.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Estabelecendo conexão com banco de dados...")
    create_db_and_tables() 
    
    print("Executando verificação inicial de ativos...")
    CoingekoFuncions.update_criptos_db_if_needed()

    print("Iniciando o servidor e o agendador de tarefas...")
    scheduler.add_job(update_criptos_db, 'interval', hours=24, id="update_assets_24h")
    scheduler.add_job(blog_catcher_worker, 'interval', minutes=5, id="blog_catcher_queue")

    scheduler.start()
    yield
    print("Desligando o agendador de tarefas...")
    scheduler.shutdown()
    
app = FastAPI(lifespan=lifespan)


# ... (seus middlewares de CORS e TrustedHost) ...
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Gitignore.FRONT_URL], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1"]
)

# ... (seus 'include_router') ...
app.include_router(createUser.router)
app.include_router(login.router)
app.include_router(operation.router)
app.include_router(stocks.router)
app.include_router(crypto.router)
app.include_router(shoping.router)
app.include_router(criptoData.router)
app.include_router(osintAnalises.router)