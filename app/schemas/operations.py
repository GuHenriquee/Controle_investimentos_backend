from pydantic import BaseModel

class Operation(BaseModel):
    amount: float
    operationType: str

class OperationResponse(BaseModel):
    amount: float
    operationType: str
    previousValue: float
    newValue: float 
