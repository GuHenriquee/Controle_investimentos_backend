from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from objects.criptoOB import CriptoProfile
from objects.whoisOB import Cripto, Whois
from objects.gitOB import Git
from funcionalities.OSINT.whois import analyze_and_create_whois_profile
from database import database
from sqlmodel import select
from funcionalities.OSINT.githubOS import githubAnalise

# Modelei uma resposta para retornar o que foi salvo
class AnalysisResponse(BaseModel):
    whois_data: Whois
    github_data: Git
    model_config = ConfigDict(from_attributes=True)


router = APIRouter()

# Mudei o status_code para 200 (OK), pois ele pode criar (201) ou atualizar (200)
@router.post("/api/osint/run-and-save-analysis/", response_model=AnalysisResponse, status_code=200)
def run_and_save_analysis(cripto: Cripto, session: database.SessionDep):

    cripto_profile_from_db = session.get(CriptoProfile, cripto.name)
    if not cripto_profile_from_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Criptomoeda com o id '{cripto.name}' não encontrada."
        )

    # 1. Executa as análises externas
    new_whois_data = analyze_and_create_whois_profile(cripto_profile_from_db.id, cripto_profile_from_db.website)
    new_git_data = githubAnalise(cripto_profile_from_db.id, cripto_profile_from_db.github_repo)

    if not new_whois_data or not new_git_data:
        details = []
        if not new_whois_data: details.append("Falha na análise Whois.")
        if not new_git_data: details.append("Falha na análise GitHub.")
        raise HTTPException(status_code=503, detail=" ".join(details))

    # 2. Lógica de "UPSERT" (O jeito certo de salvar)
    
    # Tenta pegar o objeto Whois existente
    db_whois = session.get(Whois, new_whois_data.id)
    if db_whois:
        # Se existe, atualiza os campos
        db_whois.age_in_days = new_whois_data.age_in_days
        db_whois.creation_date = new_whois_data.creation_date
        db_whois.expiration_date = new_whois_data.expiration_date
        db_whois.registrar = new_whois_data.registrar
        db_whois.has_public_contact = new_whois_data.has_public_contact
    else:
        # Se não existe, prepara para adicionar
        db_whois = new_whois_data

    # Tenta pegar o objeto Git existente
    db_git = session.get(Git, new_git_data.id)
    if db_git:
        # Se existe, atualiza os campos
        db_git.last_commit = new_git_data.last_commit
        db_git.stars_number = new_git_data.stars_number
        db_git.issues_count = new_git_data.issues_count
        db_git.forks = new_git_data.forks
        db_git.created_at = new_git_data.created_at
    else:
        # Se não existe, prepara para adicionar
        db_git = new_git_data

    # 3. Salva tudo de uma vez
    session.add(db_whois)
    session.add(db_git)
    session.commit()

    # 4. Atualiza as variáveis com os dados do banco
    session.refresh(db_whois)
    session.refresh(db_git)

    # 5. Retorna os dados que foram salvos/atualizados
    return AnalysisResponse(whois_data=db_whois, github_data=db_git)