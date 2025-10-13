from fastapi import APIRouter, HTTPException
from backend.objects.userOB import Login, Token, UserInDB
from database import database
from sqlmodel import select
from loginFuncs import LoginAndJWT

router = APIRouter()

@router.post("/api/login/", status_code=200)
def isLoged(loginCredentiasl: Login, session: database.SessionDep)-> Token:

    queryEmail = select(UserInDB).where(UserInDB.email == loginCredentiasl.email)
    existingUser = session.exec(queryEmail).first()
    
    if not existingUser or not LoginAndJWT.verify_password(loginCredentiasl.password, existingUser.password):
        raise HTTPException(status_code=401, detail="incorrect Email or password")
    
    access_token = LoginAndJWT.create_access_token(data={"sub": existingUser.email}) #"sub" abreviação de "Subject"(Sujeito). É a "reivindicação" (claim) que identifica sobre quem é o token. Em um sistema de login, o "sujeito" é o usuário.

    return Token(access_token=access_token, token_type="bearer")  #bearer token funciona como dinheiro ou um ingresso de show: qualquer pessoa que o porta (que o possui) tem o direito de usá-lo. O sistema de segurança não precisa de mais nenhuma prova, ele apenas verifica se o token em si é válido.
