from datetime import datetime, timezone
from sqlmodel import select, Session
from funcionalities.APIs.database import database
from objects.criptoOB import CriptoProfile # Importe os novos modelos
from funcionalities.APIs.coingekoData import CoingekoFuncions

def update_criptos_db():

    print(f"[{datetime.now()}] INICIANDO TAREFA AGENDADA: Atualização de todos os ativos...")
    
    with Session(database.engine) as session:
        # 1. Busca todos os IDs dos ativos que estão no banco de dados
        statement = select(CriptoProfile.id)
        asset_ids_in_db = session.exec(statement).all()
        
        updated_count = 0
        failed_count = 0

        # 2. Itera sobre cada ID e atualiza os dados
        for coin_id in asset_ids_in_db:
            try:
                cripto_to_update = session.get(CriptoProfile, coin_id)
                if not cripto_to_update:
                    continue # Pula caso o ativo tenha sido deletado durante a execução

                fresh_data = CoingekoFuncions.get_cripto_data(coin_id)
                
                if fresh_data:
                    cripto_to_update.description = fresh_data.get("description")
                    cripto_to_update.website = fresh_data.get("website")
                    cripto_to_update.twitter_handle = fresh_data.get("twitter_handle")
                    cripto_to_update.subreddit_url = fresh_data.get("subreddit_url")
                    cripto_to_update.github_repo = fresh_data.get("github_repo")
                    cripto_to_update.market_cap_rank = fresh_data.get("market_cap_rank")
                    cripto_to_update.last_updated = datetime.now(timezone.utc) # Atualiza o timestamp!
                    
                    session.add(cripto_to_update)
                    updated_count += 1
                    print(f"  - Sucesso ao atualizar '{coin_id}'")
                else:
                    failed_count += 1
                    print(f"  - Aviso: Não foram encontrados novos dados para '{coin_id}'")

            except Exception as e:
                failed_count += 1
                print(f"  - ERRO ao atualizar '{coin_id}': {e}")
        
        # 3. Salva todas as alterações no banco de uma vez
        if updated_count > 0:
            session.commit()

    print(f"[{datetime.now()}] TAREFA AGENDADA CONCLUÍDA: {updated_count} atualizados, {failed_count} falhas.")