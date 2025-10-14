from objects.userOB import UserInDB, TokenData
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from ignore import Gitignore
import jwt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from typing import Dict, Any
from sqlmodel import Session, select
from database import database


ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  #"deprecated="auto"" fará com que senhas com hashes antigos sejam atualizadas automaticamente na próxima vez que o usuário fizer login.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginAndJWT():
    
    def verify_password(password, password_in_db):
        return pwd_context.verify(password, password_in_db)


    def hashing_password(password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, Gitignore.SECRET_KEY, algorithm=ALGORITHM) #"jwt.encode" Retorna um Token
        return encoded_jwt

    # PART 2

    def get_user(username: str, session: Session):
        query = select(UserInDB).where(UserInDB.email == username)
        user = session.exec(query).first()
        return user 

    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: database.SessionDep ):

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload: Dict[str, Any] = jwt.decode(token, Gitignore.SECRET_KEY, algorithms=[ALGORITHM]) # Decodifica o jwt 
            username = payload.get("sub") # retorna o email passado
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = LoginAndJWT.get_user(username=token_data.username, session=session) #Pega o usuário pelo email
        if user is None:
            raise credentials_exception
        return user

    
    async def get_current_active_user(current_user: Annotated[UserInDB, Depends(get_current_user)],):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user