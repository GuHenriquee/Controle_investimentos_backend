from .rss_annalist import find_official_data 
from .web_scraping import find_blog
from core.database import database
from models.cripto import CriptoProfile
from sqlmodel import select, or_

def blog_catcher_worker():
 
    print("SCHEDULER (blog_catcher): Verificando fila de blogs...")

    profile_id_for_logging = "N/A" 

    with database.SessionLocal() as session:
        
        # A query "autolimpante"
        query = select(CriptoProfile).where(
            or_(
                CriptoProfile.blog == None,
                CriptoProfile.blog == "processing",
                CriptoProfile.blog == "error"
            )
        ).limit(1)
        
        profile_to_process = session.exec(query).first()
        
        if not profile_to_process:
            print("SCHEDULER: Fila de blogs vazia.")
            return

        profile_id_for_logging = profile_to_process.id
        print(f"SCHEDULER: Encontrado trabalho! Processando: {profile_id_for_logging} (Status: {profile_to_process.blog})")
        
        # --- "Blinda" o Perigoso 1 (Selenium) ---
        try:
            blog_url_encontrado = find_blog(profile_to_process.website)
            if blog_url_encontrado:
                print(f"WORKER: Blog encontrado: {blog_url_encontrado}")
                profile_to_process.blog = blog_url_encontrado
            else:
                print(f"WORKER: Blog não encontrado. Marcando como 'none'.")
                profile_to_process.blog = "none"
        except Exception as e:
            print(f"!!!!!!!!!!!!!!! ERRO CRÍTICO NO SELENIUM !!!!!!!!!!!!!!!")
            print(f"Erro: {e}. Marcando como 'error'.")
            profile_to_process.blog = "error"
        
        session.add(profile_to_process) # Adiciona o resultado do blog ao "carrinho"

        if profile_to_process.blog not in ["none", "error", "processing", None]:
            try:
                print(f"WORKER: Buscando anúncios de {profile_to_process.blog}...")
                
                find_official_data(
                    session=session, 
                    cripto_id=profile_to_process.id, 
                    feed_url=profile_to_process.blog, 
                    days_to_check=30
                )
            except Exception as e:
                print(f"!!!!!!!!!!!!!!! ERRO CRÍTICO NO FEEDPARSER (Gerente) !!!!!!!!!!!!!!!")
                print(f"Erro: {e}")        
   
    print(f"SCHEDULER: Sessão fechada e commit concluído para {profile_id_for_logging}.")