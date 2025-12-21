from pydantic import BaseModel, ConfigDict 

class shopsName(BaseModel):
    type: str
    name: str
    amount: float
    price: float
    
class ShoppingResponse(BaseModel):
        type:str
        name: str
        dataPrice: float
        amount: float
        quantity: float
        model_config = ConfigDict(from_attributes=True)