from datetime import datetime
from typing import Optional
from sqlmodel import Column, SQLModel, Field, String
from pydantic import BaseModel, ConfigDict

class CriptoRequest(BaseModel):
    coin_id: str  

class CriptoResponse(BaseModel):
    id: str
    symbol: str
    description: str
    website: Optional[str]
    twitter_handle: Optional[str]
    subreddit_url: Optional[str]
    github_repository: Optional[str]
    market_cap_rank: Optional[int]
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True) # Essencial para que o Pydantic consiga converter o objeto do banco para este modelo

class CriptoProfile(SQLModel, table=True):
    id: str = Field(primary_key=True) # O id da CoinGecko (ex: "bitcoin")
    symbol: str
    description: str = Field(sa_column=Column(String(2000))) # Aumente o tamanho para descrições longas
    website: Optional[str] = None
    twitter_handle: Optional[str] = None
    subreddit_url: Optional[str] = None
    github_repo: Optional[str] = None
    market_cap_rank: Optional[int] = None
    last_updated: datetime = Field(default_factory=...)
