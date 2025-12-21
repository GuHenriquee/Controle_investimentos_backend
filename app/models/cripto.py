from datetime import datetime
from typing import Optional
from sqlmodel import Column, SQLModel, Field, Relationship
from sqlalchemy import Text


class CriptoProfile(SQLModel, table=True):
    id: str = Field(primary_key=True)
    symbol: str
    description: Optional[str] = Field(default=None,sa_column=Column(Text))   # <- sem limite)
    website: Optional[str] = None
    twitter_handle: Optional[str] = None
    subreddit_url: Optional[str] = None
    github_repo: Optional[str] = None
    market_cap_rank: Optional[int] = None
    last_updated: datetime
    blog: Optional[str] = None
    whois_profile: "Whois" = Relationship(back_populates="cripto_profile") # type: ignore
    git_profile: "Git" = Relationship(back_populates="cripto_profile") # type: ignore
    oficial_data: "OficialData" = Relationship(back_populates="cripto_profile") # type: ignore

    
