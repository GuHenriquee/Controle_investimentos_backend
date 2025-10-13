from backend.objects.shoppingOB import Shopping, shopsName, UserInDB, ShoppingResponse
from loginFuncs import LoginAndJWT
from database import database
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
import json
import websockets
from sqlmodel import select

router = APIRouter()

@router.post("/sellOrBuy", response_model=ShoppingResponse)
async def cripto_operations(
    current_user: Annotated[UserInDB, Depends(LoginAndJWT.get_current_active_user)], session: database.SessionDep, coin: shopsName) -> ShoppingResponse:

    final_link = f"wss://stream.binance.com:9443/stream?streams={coin.name.lower()}usdt@miniTicker"
    print(f"DEBUG: URL de conexão: {final_link}")

    try:
        async with websockets.connect(final_link, open_timeout=5) as binance_websocket: 
            print("DEBUG: Conexão com Binance WebSocket estabelecida. Aguardando mensagem...")
            binance_data = await binance_websocket.recv()
            print("DEBUG: Mensagem recebida!")
    except Exception as e:
        print(f"ERRO DE WEBSOCKET: {e}") 
        raise HTTPException(status_code=503, detail=f"Erro ao comunicar com o provedor de WebSocket: {e}")
        # 503 Service Unavailable
    
    data_payload = json.loads(binance_data).get("data", {})
    current_price = float(data_payload.get("c", 0))

    if not current_price > 0:
        raise HTTPException(status_code=400, detail="Não foi possível obter um preço válido para a criptomoeda.")
    
    query = (
        select(Shopping)
        .where(Shopping.user_id == current_user.id, Shopping.name == coin.name)
        .order_by(Shopping.created_at.desc())
    )
    ultima_operacao = session.exec(query).first()
    quantidade_anterior = ultima_operacao.quantity if ultima_operacao else 0
    
    quantity_this_op = coin.amount / current_price

    if coin.type == "Buy":
        if coin.amount > current_user.patrimony:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        current_user.patrimony -= coin.amount
        nova_quantidade = quantidade_anterior + quantity_this_op
    elif coin.type == "Sell":
        if quantidade_anterior < quantity_this_op:
            raise HTTPException(status_code=400, detail="Ativos de criptomoeda insuficientes para vender")
        current_user.patrimony += coin.amount
        nova_quantidade = quantidade_anterior - quantity_this_op
    else:
        raise HTTPException(status_code=400, detail=f"Tipo de operação inválido: {coin.type}")

    nova_operacao_db = Shopping(
        type=coin.type, 
        name=coin.name, 
        dataPrice=current_price,
        amount=coin.amount, 
        quantity=nova_quantidade, 
        user_id=current_user.id
    )
    
    session.add(nova_operacao_db)
    session.add(current_user)
    session.commit()
    session.refresh(nova_operacao_db)
    
    return ShoppingResponse.model_validate(nova_operacao_db)


            