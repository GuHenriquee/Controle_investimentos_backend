from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Cripto(BaseModel):
    name: str

class WhoisOsintProfile(SQLModel, table=True):
    id: str = Field(default=None, foreign_key="criptoprofile.id", primary_key=True)
    age_in_days: Optional[int] = None
    creation_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    registrar: Optional[str] = None 
    has_public_contact: bool
    cripto_profile: "CriptoProfile" = Relationship(back_populates="osint_profile") # type: ignore
