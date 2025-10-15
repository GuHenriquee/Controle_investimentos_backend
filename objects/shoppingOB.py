from typing import Optional
from pydantic import BaseModel, ConfigDict 
from uuid import UUID, uuid4
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime, timezone

class shopsName(BaseModel):
    type: str
    name: str
    amount: float
    price: float

class Shopping(SQLModel,table =True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), nullable=False, index=True )
    type:str
    name: str
    dataPrice: float
    amount: float
    quantity: float
    user_id: Optional[UUID] = Field(default=None, foreign_key="userindb.id")
    user: Optional["UserInDB"] = Relationship(back_populates="bought")  # type: ignore

class ShoppingResponse(BaseModel):
        type:str
        name: str
        dataPrice: float
        amount: float
        quantity: float
        model_config = ConfigDict(from_attributes=True)







