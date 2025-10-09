from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import json
import websockets


router = APIRouter()

@router.websocket("/ws/{criptos}/{coin}")
async def coincapWebsocket(websocket: WebSocket, criptos, coin: str):

    await websocket.accept()
    print("Cliente conectado")

    streams = [f"{cripto.strip()}{coin}@miniTicker" for cripto in criptos.split(',')] #.strip() remove espaços em branco do início e do fim de uma string

    streams_combinados = "/".join(streams)

    final_link = f"wss://stream.binance.com:9443/stream?streams={streams_combinados}"

    async with websockets.connect(final_link) as binance_websocket:
        try:
            while True:
                binance_data = await binance_websocket.recv()
                binance_data_dict = json.loads(binance_data)
                data_payload = binance_data_dict.get("data", {})

                frontend_data = {
                "symbol": data_payload.get("s"),          
                "current_price": float(data_payload.get("c")),     
                "high_24h": float(data_payload.get("h")),   
                "low_24h": float(data_payload.get("l"))     
                }

                await websocket.send_json(frontend_data)
        except WebSocketDisconnect:
            print("Cliente desconectado")
            