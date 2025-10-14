from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
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