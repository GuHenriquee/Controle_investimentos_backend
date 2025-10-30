from datetime import datetime
from typing import Optional
from sqlalchemy import String
from sqlmodel import Column, SQLModel, Field, Relationship


class OsintData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_name: str = Field(index=True)                             # ex: "bitcoin", "cardano"
    source: str                                                     # ex: "Twitter", "CoinTelegraph", "Reddit"
    content: str                                                    # O texto do tweet, o corpo do artigo
    url: str                                                        # O link para a fonte original
    collected_at: datetime = Field(default_factory=...)

# Tabela para guardar os insights gerados pela IA
class AiInsight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_name: str = Field(index=True)
    sentiment: str       # ex: "Muito Positivo", "Negativo", "Neutro"
    summary: str         # Um resumo de 2 linhas do que aconteceu
    risk_level: str      # ex: "Baixo", "Médio", "Alto"
    keywords: str        # ex: "parceria,SEC,hack,mainnet"
    source_data_id: int = Field(foreign_key="osintdata.id") # Link para o dado bruto
    processed_at: datetime = Field(default_factory=...)

class OficialData(SQLModel, table=True):
    link: str = Field(primary_key=True) 
    title: str
    date: datetime
    summary: str = Field(sa_column=Column(String(2000))) 
    cripto_id: str = Field(foreign_key="criptoprofile.id", index=True)
    cripto_profile: "CriptoProfile" = Relationship(back_populates="oficial_data") # type: ignore
