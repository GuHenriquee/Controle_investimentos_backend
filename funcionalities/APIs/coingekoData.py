from pycoingecko import CoinGeckoAPI
from sqlmodel import Session, select
from datetime import datetime, timedelta, timezone
from funcionalities.APIs.database import database
from objects.criptoOB import CriptoProfile

cg = CoinGeckoAPI()

class CoingekoFuncions():
    def get_cripto_data(coin_id: str):

        try:
            data = cg.get_coin_by_id(
                id=coin_id, 
                localization='false', 
                tickers='false', 
                market_data='true', 
                community_data='true', 
                developer_data='true')
            
            # Tratamento para evitar erro se a lista de links estiver vazia
            homepage = data.get("links", {}).get("homepage", [])
            github = data.get("links", {}).get("repos_url", {}).get("github", [])

            profile = {
                "id": data.get("id"),
                "symbol": data.get("symbol"),
                "description": data.get("description", {}).get("en", "N/A"),
                "website": homepage[0] if homepage else None,
                "twitter_handle": data.get("links", {}).get("twitter_screen_name"),
                "subreddit_url": data.get("links", {}).get("subreddit_url"),
                "github_repo": github[0] if github else None,
                "market_cap_rank": data.get("market_cap_rank"),
            }
            return profile
        except Exception as e:
            print(f"Erro ao buscar perfil para '{coin_id}': {e}")
            return None
        

    def update_criptos_db_if_needed():
        
        print(f"[{datetime.now()}] INICIANDO VERIFICAÇÃO DE ATIVOS DESATUALIZADOS...")
        
        with database.SessionLocal() as session:
            statement = select(CriptoProfile)
            criptos_in_db = session.exec(statement).all()
            
            updated_count = 0
            failed_count = 0
            
            twenty_four_hours_ago = datetime.now(timezone.utc) - timedelta(hours=24)

    #Objetos datetime, o símbolo < não significa "menor" no sentido numérico, mas sim "anterior no tempo" ou "aconteceu antes de".
            for cripto in criptos_in_db:
                if cripto.last_updated.replace(tzinfo=timezone.utc) < twenty_four_hours_ago: #"tzinfo" timezone info
                    print(f"  - Ativo '{cripto.id}' está desatualizado. Atualizando...")
                    try:
                        # O resto da sua lógica permanece o mesmo
                        fresh_data = CoingekoFuncions.get_cripto_data(cripto.id)
                        
                        if fresh_data:
                            cripto.description = fresh_data.get("description")
                            cripto.website = fresh_data.get("website")
                            cripto.market_cap_rank = fresh_data.get("market_cap_rank")
                            cripto.last_updated = datetime.now(timezone.utc) 
                            
                            session.add(cripto)
                            updated_count += 1
                        else:
                            failed_count += 1

                    except Exception as e:
                        failed_count += 1
                        print(f"  - ERRO ao processar '{cripto.id}': {e}")

            if updated_count > 0:
                print(f"Salvando {updated_count} atualizações no banco de dados...")
                session.commit()

        print(f"[{datetime.now()}] VERIFICAÇÃO CONCLUÍDA: {updated_count} atualizados, {failed_count} falhas.")