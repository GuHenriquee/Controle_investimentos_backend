# Em funcionalities/OSINT/rssAnalysis.py
# (Esta versão é a correta. NÃO a mude.)

from typing import List
import feedparser
from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from objects.osintOB import OficialData

def official_data(session: Session, cripto_id: str, feed_url: str, days_to_check=7) -> None:
    
    print(f"Buscando anúncios em: {feed_url}")
    feed = feedparser.parse(feed_url)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_check)
    
    new_posts_to_add: List[OficialData] = [] 
    print(f"Filtrando por notícias dos últimos {days_to_check} dias (desde {cutoff_date.date()})...")

    for entry in feed.entries:
        published_timestamp = entry.get("published_parsed")
        
        if published_timestamp:
            published_date = datetime(*published_timestamp[:6], tzinfo=timezone.utc)
            
            if published_date >= cutoff_date:
                link = entry.link
                
                # Usa a sessão SÓ para checar duplicatas
                existing_post = session.get(OficialData, link)

                if not existing_post:
                    print(f"NOVO POST ENCONTRADO (para adicionar): {entry.title}")
                    oficialData = OficialData(
                        link=link,
                        title=entry.title,
                        summary=entry.get("summary", "N/A"),
                        date=published_date,
                        cripto_id=cripto_id
                    )
                    new_posts_to_add.append(oficialData)
            else:
                print(f"\nParando a busca (post de {published_date.date()} é muito antigo).")
                break 

    if new_posts_to_add:
        print(f"Adicionando {len(new_posts_to_add)} novos posts à sessão (carrinho)...")
        session.add_all(new_posts_to_add) # <-- Coloca no carrinho
        # NENHUM COMMIT AQUI!
    else:
        print("Nenhum post *novo* encontrado no período.")