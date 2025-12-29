from typing import List
import feedparser
import re 
from datetime import datetime, timedelta, timezone
from models.osint import OficialData

def clean_html(raw_html: str) -> str:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    
    cleantext = " ".join(cleantext.split())
    
    return cleantext

def find_official_data(cripto_id: str, feed_url: str, days_to_check=30) -> List[OficialData]:
    
    print(f"Buscando anúncios em: {feed_url}")
    try:
        feed = feedparser.parse(feed_url)
    except Exception as e:
        print(f"Erro ao analisar o feed RSS de {cripto_id}: {e}")
        return []

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_check)
    
    new_posts_to_add: List[OficialData] = [] 
    
    if not feed.entries:
        print(f"Feed de {cripto_id} não contém 'post ou noticias (entries)'. Pulando.")
        return

    print(f"Filtrando por notícias dos últimos {days_to_check} dias...")
    for entry in feed.entries:
        published_timestamp = entry.get("published_parsed") or entry.get("updated_parsed")
        
        if published_timestamp:
            published_date = datetime(*published_timestamp[:6], tzinfo=timezone.utc)
            
            if published_date >= cutoff_date:
                summary_clean = entry.get("summary", "N/A")
                summary_clean = clean_html(summary_clean)[:1000]

                oficialData = OficialData(
                    link=entry.link, 
                    title=entry.title,
                    summary=summary_clean,
                    date=published_date, 
                    cripto_id=cripto_id
                )
                new_posts_to_add.append(oficialData)
            else:
                break
    return new_posts_to_add