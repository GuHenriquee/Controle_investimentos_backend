from fastapi import APIRouter, Depends, HTTPException
from objects.criptoOB import CriptoProfile
from objects.whoisOB import WhoisOsintProfile, Cripto
from funcionalities.criptoSiteOsint import analyze_and_create_whois_profile
from database import database
from sqlmodel import select

router = APIRouter()

@router.post("/api/whois/", status_code=201)
def siteChecker(cripto:Cripto, session: database.SessionDep) -> WhoisOsintProfile:

    query = select(CriptoProfile).where(CriptoProfile.id == cripto.name)
    cripto_profile_from_db = session.exec(query).first()

    if not cripto_profile_from_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Criptomoeda com o id '{cripto.name}' não encontrada no banco de dados."
        )

    return analyze_and_create_whois_profile(cripto_profile_from_db.id, cripto_profile_from_db.website)


