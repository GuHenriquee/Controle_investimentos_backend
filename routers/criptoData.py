from datetime import datetime, timezone
from typing import Annotated
from sqlmodel import select, Session
from fastapi import APIRouter, Depends, HTTPException
from database import database
from objects.criptoOB import CriptoResponse, CriptoRequest, CriptoProfile # Importe os novos modelos
from objects.userOB import UserInDB 
from loginFuncs import LoginAndJWT
from coingekoData import get_cripto_data


router = APIRouter()

@router.post("/assets/add", response_model=CriptoResponse, status_code=201)
def add_new_cripto_to_monitor(name: CriptoRequest, session: database.SessionDep, 
                             current_user: Annotated[UserInDB, Depends(LoginAndJWT.get_current_active_user)]) -> CriptoProfile:
   
    coin_id = name.coin_id.lower()
    print(f"Usuário '{current_user.name}' solicitou adicionar o ativo: {coin_id}")

    # 1. Verifica se o ativo já existe no banco de dados para evitar duplicatas
    existing_profile = session.get(CriptoProfile, coin_id)
    if existing_profile:
        raise HTTPException(status_code=409, detail=f"Ativo '{coin_id}' já está sendo monitorado.")

    # 2. Busca os dados do perfil na API da CoinGecko
    new_profile_data = get_cripto_data(coin_id)
    if not new_profile_data:
        raise HTTPException(status_code=404, detail=f"Não foi possível encontrar o ativo '{coin_id}' na CoinGecko.")

    # 3. Cria um novo objeto AssetProfile com os dados obtidos
    new_asset = CriptoProfile(
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

    # 4. Salva o novo ativo no banco de dados
    session.add(new_asset)
    session.commit()
    session.refresh(new_asset)

    print(f"Ativo '{coin_id}' adicionado com sucesso ao banco de dados.")
    
    return new_asset



