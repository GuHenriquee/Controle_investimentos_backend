from fastapi import APIRouter

from api.v1.endpoints import create_user, cripto_data, crypto, login, stocks, shopping, operation, osint_analises

api_router = APIRouter()

api_router.include_router(create_user.router, prefix="/create_user", tags=["Create User"])
api_router.include_router(login.router, prefix="/login", tags=["Login"])
api_router.include_router(operation.router, prefix="/operations", tags=["Operations"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
api_router.include_router(crypto.router, prefix="/crypto", tags=["Crypto"])
api_router.include_router(shopping.router, prefix="/shopping", tags=["Shopping"])
api_router.include_router(cripto_data.router, prefix="/cripto_data", tags=["Cripto Data"])
api_router.include_router(osint_analises.router, prefix="/osint_analises", tags=["OSINT Analyses"])
