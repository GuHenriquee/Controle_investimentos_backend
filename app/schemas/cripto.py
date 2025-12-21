from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class CriptoRequest(BaseModel):
    coin_id: str  

class CriptoSearch(BaseModel):
    name: str

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