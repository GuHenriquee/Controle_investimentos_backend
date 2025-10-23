import whois
from datetime import datetime, timezone
from objects.whoisOB import Whois

def analyze_and_create_whois_profile(cripto_id: str, domain: str):
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

