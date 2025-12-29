from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.cripto import CriptoProfile # Importe os novos modelos
from schemas.cripto import CriptoRequest
from services.coingeko_data import CoingekoFuncions
from api.deps import SessionDep, addToDB

router = APIRouter()

@router.post("/", status_code=201)
def add_new_cripto_to_monitor(name: CriptoRequest, session: SessionDep ) -> CriptoProfile:
   
    coin_id = name.coin_id

    existing_profile = session.get(CriptoProfile, coin_id)
    if existing_profile:
        raise HTTPException(status_code=409, detail=f"Ativo '{coin_id}' já está sendo monitorado.")

    new_profile_data = CoingekoFuncions.get_cripto_data(coin_id)
    if not new_profile_data:
        raise HTTPException(status_code=404, detail=f"Não foi possível encontrar o ativo '{coin_id}' na CoinGecko.")

    new_cripto = CriptoProfile(
        id=new_profile_data["id"],
        symbol=new_profile_data["symbol"],
        description=new_profile_data["description"],
        website=new_profile_data["website"],
        twitter_handle=new_profile_data["twitter_handle"],
        subreddit_url=new_profile_data["subreddit_url"],
        github_repo=new_profile_data["github_repo"],
        market_cap_rank=new_profile_data["market_cap_rank"],
        last_updated=datetime.now(timezone.utc)
    )

    addToDB(new_cripto, session)
    

    print(f"Ativo '{coin_id}' adicionado com sucesso ao banco de dados.")
    
    return new_cripto



