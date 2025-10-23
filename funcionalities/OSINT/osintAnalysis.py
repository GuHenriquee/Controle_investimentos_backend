import whois
from datetime import datetime, timezone
from objects.analiseOB import Whois, Git
from github import Github
from ignore import Gitignore
from github import Auth
from urllib.parse import urlparse


class PrimaryAnalysis():

    def whoisAnalize(cripto_id: str, domain: str):
        try:
            informacoes = whois.whois(domain)

            # 1. Data de Criação
            creation_date_raw = informacoes.creation_date
            creation_date_clean = creation_date_raw[0] if isinstance(creation_date_raw, list) else creation_date_raw

            # 2. Data de Expiração
            expiration_date_raw = informacoes.expiration_date
            expiration_date_clean = expiration_date_raw[0] if isinstance(expiration_date_raw, list) else expiration_date_raw

            # 3. A empresa que foi usada para comprar o domínio
            registrar_clean = informacoes.registrar

            # 4. Contato Público
            emails_raw = informacoes.emails
            has_public_contact_clean = bool(emails_raw and isinstance(emails_raw, list) and len(emails_raw) > 0)

            # 5. Idade em Dias (Cálculo)
            age_in_days_clean = None
            if creation_date_clean:
                creation_date_aware = creation_date_clean.replace(tzinfo=timezone.utc)
                now_aware = datetime.now(timezone.utc)
                age_in_days_clean = (now_aware - creation_date_aware).days


            osint_profile = Whois(
                id=cripto_id,  
                age_in_days=age_in_days_clean,
                creation_date=creation_date_clean,
                expiration_date=expiration_date_clean,
                registrar=registrar_clean,
                has_public_contact=has_public_contact_clean
            )
            
            return osint_profile

        except Exception as e:
            print(f"Falha ao analisar o domínio '{domain}': {e}")
            return None



    def githubAnalize(cripto_id: str, url: str)->Git | None :

        auth = Auth.Token(Gitignore.GITHUB_TOKEN)
        g = Github(auth=auth)
        
        try:
            path = urlparse(url).path 
            repo_name = path.strip("/")
            repo = g.get_repo(repo_name)

            git_on_db = Git(
                id = cripto_id,
                last_commit = repo.pushed_at,
                stars_number = repo.stargazers_count,
                issues_count = repo.open_issues_count,
                forks = repo.forks_count,
                created_at = repo.created_at
            )
            return git_on_db
            
        except Exception as e:
            print(e)
            return None    
