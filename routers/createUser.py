from backend.objects.userOB import UserInDB, UserCreate, UserResponse
from database import database
from sqlmodel import select
from fastapi import HTTPException, APIRouter
from loginFuncs import LoginAndJWT

router = APIRouter()

@router.post("/api/register/", status_code=201) #201 = created
def create_user(user: UserCreate, session: database.SessionDep)-> UserResponse:

    query = select(UserInDB).where(UserInDB.email == user.email) #criando consulta
    existing_user = session.exec(query).first()                  #executando consulta

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserInDB(
        name=user.name,
        email=user.email,
        password= LoginAndJWT.hashing_password(user.password),  
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    print("Usuário para 'salvar' no banco de dados:", db_user)

    return db_user