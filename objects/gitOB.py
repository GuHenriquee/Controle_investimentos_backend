from sqlmodel import SQLModel, Field, Relationship, Column
from datetime import datetime
from sqlalchemy import DateTime # Importe o DateTime da SQLAlchemy

class Git(SQLModel, table=True):
    id: str = Field(default=None, foreign_key="criptoprofile.id", primary_key=True)
    last_commit: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    stars_number: int
    issues_count: int
    forks: int
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    cripto_profile: "CriptoProfile" = Relationship(back_populates="git_profile") # type: ignore