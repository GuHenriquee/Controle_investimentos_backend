from funcionalities.OSINT.rssAnalysis import official_data
from funcionalities.OSINT.webScraping import find_blog
from funcionalities.APIs.database import database
from objects.criptoOB import CriptoProfile
from objects.osintOB import OficialData
from sqlmodel import select, Session
from typing import List

def _run_blog_catcher_task(session: Session, profile: CriptoProfile):

    blog_url_encontrado = None
    try:
        print(f"WORKER: Rodando Selenium para {profile.id}...")
        blog_url_encontrado = find_blog(profile.website)
    except Exception as e:
        print(f"Erro ao tentar encontrar blog para {profile.id}: {e}")
        blog_url_encontrado = None 

    # --- ETAPA 2: ATUALIZAR O PERFIL ---
    if blog_url_encontrado:
        profile.blog = blog_url_encontrado
        print(f"WORKER: Blog encontrado: {blog_url_encontrado}")
    else:
        profile.blog = "none" 
        print(f"WORKER: Blog não encontrado. Marcando como 'none'.")
    
    session.add(profile) 

    # --- ETAPA 3: O TRABALHO PERIGOSO 2 (FEEDPARSER) ---
    if profile.blog and profile.blog != "none":
        try:
            print(f"WORKER: Buscando anúncios de {profile.blog}...")
            official_data(session=session,cripto_id=profile.id, feed_url=profile.blog, days_to_check=30)
        except Exception as e:
            print(f"Erro ao buscar posts para {profile.id}: {e}")
            

def blog_catcher_worker():
   
    print("SCHEDULER (blog_catcher): Verificando fila de blogs...")
    
    with database.SessionLocal() as session:
        
        query = select(CriptoProfile).where(CriptoProfile.blog == None).limit(1)
        profile_to_process = session.exec(query).first()
        
        if profile_to_process:
            print(f"SCHEDULER: Encontrado trabalho! Processando: {profile_to_process.id}")
            
            profile_to_process.blog = "processing"
            session.add(profile_to_process)
            session.commit()
            
            try:
                _run_blog_catcher_task(session, profile_to_process)
                session.commit()
                print(f"SCHEDULER: Trabalho para {profile_to_process.id} salvo com sucesso.")
                
            except Exception as e:
                print(f"Erro: {e}. Revertendo e marcando {profile_to_process.id} como 'error'.")
                session.rollback() 
                
                # 2. Re-abre a sessão para "travar permanentemente" o item
                with database.SessionLocal() as lock_session:
                    profile_to_lock = lock_session.get(CriptoProfile, profile_to_process.id)
                    if profile_to_lock:
                        profile_to_lock.blog = "error" 
                        lock_session.add(profile_to_lock)
                        lock_session.commit()
                
        else:
            print("SCHEDULER (blog_catcher): Fila de blogs vazia.")