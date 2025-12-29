from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.web_scraping import find_blog

router = APIRouter()

# Modelo simples para o corpo da requisição
class UrlRequest(BaseModel):
    url: str

@router.post("/", status_code=200)
def discover_rss_url(payload: UrlRequest):
    """
    Recebe a URL da Home de um projeto e tenta descobrir o RSS.
    """
    if not payload.url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL deve começar com http ou https")

    rss_url = find_blog(payload.url)

    if rss_url:
        return {
            "status": "success",
            "original_url": payload.url,
            "rss_found": rss_url
        }
    else:
        return {
            "status": "failed",
            "message": "Nenhum feed RSS encontrado automaticamente.",
            "original_url": payload.url
        }