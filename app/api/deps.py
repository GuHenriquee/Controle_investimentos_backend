from typing import Annotated
from fastapi import Depends
from requests import Session
from models.user import UserInDB
from services.login_service import LoginAndJWT
from core.database import database

SessionDep = Annotated[Session, Depends(database.get_session)]
CurrentUser = Annotated[UserInDB, Depends(LoginAndJWT.get_current_active_user)]
