from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from urllib.parse import urljoin, urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_blog(base_url: str) -> Optional[str]:

    print(f"🕵️‍♂️ Iniciando detetive Selenium em: {base_url}")
    
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc

    # --- Atalhos Rápidos (Evita abrir o Chrome se não precisar) ---
    if "medium.com" in domain:
        return f"{parsed_url.scheme}://{domain}/feed{parsed_url.path}"
    
    if "substack.com" in domain:
        return f"{base_url.rstrip('/')}/feed"

    # --- Configuração do Chrome (Blindado para Servidor) ---
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox") # CRÍTICO para Docker/Linux
    options.add_argument("--disable-dev-shm-usage") # CRÍTICO para memória
    options.add_argument("--log-level=3")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(options=options) 
        driver.set_page_load_timeout(15) # Não deixa travar eternamente
        driver.get(base_url)

        # --- Pista 1: O Padrão Ouro (<link type="application/rss+xml">) ---
        print("🔍 Procurando meta tag RSS (Padrão Ouro)...")
        try:
            wait = WebDriverWait(driver, 5) # 5s é suficiente
            rss_link_tag = wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 'link[rel="alternate"][type="application/rss+xml"]'
                ))
            )
            feed_url = rss_link_tag.get_attribute('href')
            if feed_url:
                print(f"✅ ACHOU (Meta Tag): {feed_url}")
                return urljoin(base_url, feed_url)
        except TimeoutException:
            print("❌ Meta tag não encontrada.")

        # --- Pista 2: Varredura de Links Visíveis (<a>) ---
        print("🔍 Varrendo links da página (href)...")
        try:
            possible_links = driver.find_elements(By.TAG_NAME, "a")
            for link in possible_links:
                try:
                    href = link.get_attribute("href")
                    if href:
                        # Filtros para evitar falso positivo
                        h_lower = href.lower()
                        if any(x in h_lower for x in ["/rss", "/feed", ".xml"]) and "comments" not in h_lower:
                            print(f"✅ ACHOU (Link visível): {href}")
                            return urljoin(base_url, href)
                except StaleElementReferenceException:
                    continue # Elemento mudou, pula pro próximo
        except Exception:
            pass

        # --- Pista 3: Força Bruta (Tentativa Direta) ---
        # Se nada funcionou, tenta acessar /feed ou /blog/feed na marra
        print("🔨 Tentando Força Bruta (/feed)...")
        common_paths = ["/feed", "/rss", "/blog/feed", "/news/feed"]
        
        for path in common_paths:
            guess_url = urljoin(base_url, path)
            try:
                driver.get(guess_url)
                # Se a página carregar e tiver XML no código fonte
                page_source = driver.page_source[:500] # Olha só o começo
                if "<?xml" in page_source or "<rss" in page_source or "<feed" in page_source:
                    print(f"✅ ACHOU (Força Bruta): {guess_url}")
                    return guess_url
            except Exception:
                continue

    except Exception as e:
        print(f"🚨 Erro crítico no Selenium: {e}")
    
    finally:
        if driver:
            driver.quit()

    print(f"❌ Desistindo. Nenhum RSS encontrado para {base_url}.")
    return None