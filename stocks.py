import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websockets
from ignore import Gitignore

# 1. Em vez de 'FastAPI()', criamos um 'APIRouter()'
router = APIRouter()

# 2. Usamos o decorador '@router.websocket' em vez de '@app.websocket'
@router.websocket("/ws/realtimestocks/{tickers}")
async def websocket_realtimestocks_proxy(client_websocket: WebSocket, tickers: str):
  
    await client_websocket.accept()
    
    stocks_to_subscribe = [stock.strip() for stock in tickers.split(',')]
    
    finnhub_uri = f"wss://ws.finnhub.io?token={Gitignore.FINNHUB_API_KEY}"
    
    try:
        async with websockets.connect(finnhub_uri) as finnhub_websocket:
            print("Conectado ao servidor da Finnhub.")
            
            for stock in stocks_to_subscribe:
                await finnhub_websocket.send(json.dumps({'type':'subscribe', 'symbol': stock}))
                print(f"Inscrito em {stock}...")

            while True:
                message_from_finnhub = await finnhub_websocket.recv()
                await client_websocket.send_text(message_from_finnhub)

    except WebSocketDisconnect:
        print(f"Cliente desconectado (tickers: {tickers}).")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")