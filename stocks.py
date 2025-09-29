import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import websockets
from ignore import Gitignore

app = FastAPI()

# A URL agora inclui um parâmetro de caminho para os tickers
@app.websocket("/ws/realtimestocks/{tickers}")
async def websocket_realtimestocks_proxy(client_websocket: WebSocket, tickers: str):

    await client_websocket.accept()
    
    # Transforma a string "PETR4.SA,VALE3.SA" em uma lista ["PETR4.SA", "VALE3.SA"]
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