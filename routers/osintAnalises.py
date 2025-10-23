from fastapi import APIRouter, Depends, HTTPException
from objects.criptoOB import CriptoProfile
from objects.whoisOB import Cripto
from backend.funcionalities.OSINT.whois import analyze_and_create_whois_profile
from database import database
from sqlmodel import select
from funcionalities.OSINT.githubOS import githubAnalise

router = APIRouter()

@router.post("/api/whois/", status_code=201)
def siteChecker(cripto:Cripto, session: database.SessionDep):

    query = select(CriptoProfile).where(CriptoProfile.id == cripto.name)
    cripto_profile_from_db = session.exec(query).first()

    if not cripto_profile_from_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Criptomoeda com o id '{cripto.name}' não encontrada no banco de dados."
        )
    
    whoisAnalise = analyze_and_create_whois_profile(cripto_profile_from_db.id, cripto_profile_from_db.website)
    gitAnalise = githubAnalise(cripto_profile_from_db.id, cripto_profile_from_db.github_repo)


    session.add(whoisAnalise,gitAnalise)
    session.commit()
    session.refresh(whoisAnalise,gitAnalise)

    return 


