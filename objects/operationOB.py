from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from sqlmodel import Relationship, SQLModel, Field

class Operation(BaseModel):
    amount: float
    operationType: str

class OperationResponse(BaseModel):
    amount: float
    operationType: str
    previousValue: float
    newValue: float 

class OperationInDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    operationType: str
    previousValue: float
    newValue: float
    user_id: Optional[UUID] = Field(default=None, foreign_key="userindb.id")
    user: Optional["UserInDB"] = Relationship(back_populates="historic") # type: ignore