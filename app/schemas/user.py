from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    patrimony: float

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class Token (BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Login(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    patrimony: float