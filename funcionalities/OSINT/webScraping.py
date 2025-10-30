from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from urllib.parse import urljoin, urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_blog(base_url: str) -> str | None:

    print(f"Iniciando busca com Selenium para: {base_url}")
    
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc

    if "medium.com" in domain:
        feed_url = f"{parsed_url.scheme}://{domain}/feed{parsed_url.path}"
        print(f"Site é Medium. Tentando URL: {feed_url}")
        return feed_url

    if "substack.com" in domain:
        feed_url = f"{base_url.rstrip('/')}/feed"
        print(f"Site é Substack. Tentando URL: {feed_url}")
        return feed_url

    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")                          # Faça tudo em segundo plano
    options.add_argument("--log-level=3")                       # Não poluir seu terminal com mensagens de status inúteis
    options.add_argument("accept-language=en-US,en;q=0.9")      # Site em Inglês (mais provável de ter o RSS)
    driver = None
    
    try:
        driver = webdriver.Chrome(options=options) 
        driver.get(base_url)

        print("Aguardando Pista 1 (Padrão Ouro) carregar (até 10s)...")
        wait = WebDriverWait(driver, 10)                        # Cria um "vigia" que espera no máximo 10 segundos
        
        rss_link_tag = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 'link[rel="alternate"][type="application/rss+xml"]')))
        
        feed_url = rss_link_tag.get_attribute('href')
        if feed_url:
            print(f"Pista 1 (Padrão Ouro) encontrada: {feed_url}")
            return urljoin(base_url, feed_url)

    except TimeoutException: # Se deu 10 segundos e o elemento não apareceu, o vigia desiste
        print("Pista 1 falhou (Timeout). Procurando Pista 2...")
    except Exception as e:# Pega outros erros (ex: site não existe)
        print(f"Erro ao analisar {base_url} com Selenium: {e}")
        if driver:
            driver.quit()
        return None

    # --- Pista 2 (Chute Educado) ---
    # (Só roda se a Pista 1 falhou)
    try:
        possible_links = driver.find_elements(By.TAG_NAME, "a")
        for link in possible_links:
            href = link.get_attribute("href")
            if href and ("rss" in href.lower() or "feed" in href.lower() or ".xml" in href.lower()):
                print(f"Pista 2 (Chute Educado) encontrada: {href}")
                return urljoin(base_url, href)
    except Exception as e:
        print(f"Erro ao procurar Pista 2: {e}")
        pass # Ignora erros aqui para garantir que o 'finally' rode

    finally:
        if driver:
            driver.quit() # Sempre feche o navegador robô

    print(f"Nenhum feed RSS encontrado para {base_url}.")
    return None

