from typing import List
import feedparser
from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from models.osint import OficialData

def find_official_data(session: Session, cripto_id: str, feed_url: str, days_to_check=7) -> None:
    
    print(f"Buscando anúncios em: {feed_url}")
    feed = feedparser.parse(feed_url)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_check)
    
    new_posts_to_add: List[OficialData] = [] 
    
    if feed.bozo:
        print(f"AVISO: Feed de {cripto_id} está mal formatado (bozo=True).")
    if not feed.entries:
        print(f"Feed de {cripto_id} não contém 'entries'. Pulando.")
        return

    print(f"Filtrando por notícias dos últimos {days_to_check} dias...")
    for entry in feed.entries:
        published_timestamp = entry.get("published_parsed")
        
        if published_timestamp:
            published_date = datetime(*published_timestamp[:6], tzinfo=timezone.utc)
            
            if published_date >= cutoff_date:
                link = entry.link
                existing_post = session.get(OficialData, link)

                if not existing_post:
                    print(f"NOVO POST ENCONTRADO (para adicionar): {entry.title}")
                    oficialData = OficialData(
                        link=link, title=entry.title,
                        summary=entry.get("summary", "N/A"),
                        date=published_date, cripto_id=cripto_id
                    )
                    new_posts_to_add.append(oficialData)
            else:
                break

    if new_posts_to_add:
        print(f"Adicionando {len(new_posts_to_add)} novos posts à sessão (carrinho)...")
        session.add_all(new_posts_to_add) # <-- Coloca no carrinho
    else:
        print("Nenhum post *novo* encontrado no período.")
    
    # NENHUM COMMIT AQUI!