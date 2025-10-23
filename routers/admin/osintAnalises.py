from fastapi import APIRouter, HTTPException
from objects.criptoOB import CriptoProfile
from objects.analiseOB import Cripto, Whois,Git, AnalysisResponse
from funcionalities.OSINT.osintAnalysis import PrimaryAnalysis 
from funcionalities.APIs.database import database


router = APIRouter()

@router.post("/api/osint/run-and-save-analysis/", response_model=AnalysisResponse, status_code=200)
def run_and_save_analysis(cripto: Cripto, session: database.SessionDep):

    cripto_profile_from_db = session.get(CriptoProfile, cripto.name)
    if not cripto_profile_from_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Criptomoeda com o id '{cripto.name}' não encontrada."
        )

    new_whois_data = PrimaryAnalysis.whoisAnalize(cripto_profile_from_db.id, cripto_profile_from_db.website)
    new_git_data = PrimaryAnalysis.githubAnalize(cripto_profile_from_db.id, cripto_profile_from_db.github_repo)

    if not new_whois_data or not new_git_data:
        details = []
        if not new_whois_data: details.append("Falha na análise Whois.")
        if not new_git_data: details.append("Falha na análise GitHub.")
        raise HTTPException(status_code=503, detail=" ".join(details))

    
    db_whois = session.get(Whois, new_whois_data.id)
    if db_whois:
        db_whois.age_in_days = new_whois_data.age_in_days
        db_whois.creation_date = new_whois_data.creation_date
        db_whois.expiration_date = new_whois_data.expiration_date
        db_whois.registrar = new_whois_data.registrar
        db_whois.has_public_contact = new_whois_data.has_public_contact
    else:
        db_whois = new_whois_data

    db_git = session.get(Git, new_git_data.id)
    if db_git:
        db_git.last_commit = new_git_data.last_commit
        db_git.stars_number = new_git_data.stars_number
        db_git.issues_count = new_git_data.issues_count
        db_git.forks = new_git_data.forks
        db_git.created_at = new_git_data.created_at
    else:
        db_git = new_git_data

    session.add(db_whois)
    session.add(db_git)
    session.commit()
 
    session.refresh(db_whois)
    session.refresh(db_git)

    return AnalysisResponse(whois_data=db_whois, github_data=db_git)