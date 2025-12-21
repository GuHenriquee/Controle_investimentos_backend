from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from services.blog_data_catcher import blog_catcher_worker
from core.database import database 
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from services.scheduler import update_criptos_db
from services.coingeko_data import CoingekoFuncions
from sqlmodel import SQLModel 
from core.config import settings
from api.v1.api import api_router

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
    scheduler.add_job(blog_catcher_worker, 'interval', minutes=2, id="blog_catcher_queue")

    scheduler.start()
    yield
    print("Desligando o agendador de tarefas...")
    scheduler.shutdown()
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONT_URL], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1"]
)

app.include_router(api_router, prefix="/api/v1")