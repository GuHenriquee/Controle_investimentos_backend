from models.osint import OficialData
from fastapi import  APIRouter
from api.deps import SessionDep, addToDB
from services.rss_annalist import find_official_data

router = APIRouter()

@router.post("/", status_code=201) #201 = created
def create_user(cripto_id: str, feed_url: str, session: SessionDep):

    posts = find_official_data(cripto_id, feed_url)

    saved_count = 0
    
    for post in posts:
        existing_post = session.get(OficialData, post.link)
        if not existing_post:
            try:
                addToDB(post, session)
                saved_count += 1
                print(f"Post adicionado ao banco de dados: {post.title}")
            except Exception as e:
                print(f"Erro ao adicionar post: {e}")
                session.rollback()
        else:
            print(f"Post já existe no banco de dados: {post.link}")

    return {
        "status": "already up to date" if existing_post else "success", 
        "found": len(posts), 
        "saved_new": saved_count,
        "data": posts
    }