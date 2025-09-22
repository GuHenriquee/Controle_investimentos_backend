from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from ignore import Gitignore
import jwt


ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  #"deprecated="auto"" fará com que senhas com hashes antigos sejam atualizadas automaticamente na próxima vez que o usuário fizer login.

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

        encoded_jwt = jwt.encode(to_encode, Gitignore.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt