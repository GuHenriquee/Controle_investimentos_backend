from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime 

class Cripto(BaseModel):
    name: str

class Whois(SQLModel, table=True):
    id: str = Field(default=None, foreign_key="criptoprofile.id", primary_key=True)
    age_in_days: Optional[int] = None
    creation_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    registrar: Optional[str] = None 
    has_public_contact: bool
    cripto_profile: "CriptoProfile" = Relationship(back_populates="whois_profile") # type: ignore

class Git(SQLModel, table=True):
    id: str = Field(default=None, foreign_key="criptoprofile.id", primary_key=True)
    last_commit: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    stars_number: int
    issues_count: int
    forks: int
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    cripto_profile: "CriptoProfile" = Relationship(back_populates="git_profile") # type: ignore

class AnalysisResponse(BaseModel):
    whois_data: Whois
    github_data: Git
    model_config = ConfigDict(from_attributes=True)
