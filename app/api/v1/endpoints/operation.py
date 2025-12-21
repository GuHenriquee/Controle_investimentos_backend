from fastapi import APIRouter
from models.operations import OperationInDB
from schemas.operations import Operation, OperationResponse
from services.operations_service import Operations
from api.deps import SessionDep, CurrentUser

router = APIRouter()

@router.post("/api/operation/", status_code=201)
def operator(operation: Operation, session: SessionDep, 
             current_user: CurrentUser)-> OperationResponse:
    

    if (operation):
        if (operation.operationType == "Retirar"):
            result = Operations.minus(current_user.patrimony, operation.amount)
        else:
            result = Operations.sum(current_user.patrimony, operation.amount)

    lastOperation = OperationInDB(
        amount = operation.amount,
        operationType = operation.operationType,
        previousValue = current_user.patrimony,
        newValue= result,
        user_id= current_user.id
    )

    current_user.patrimony = lastOperation.newValue
    
    session.add(lastOperation)
    session.add(current_user)
    session.commit()
    session.refresh(lastOperation)
    session.refresh(current_user)

    return lastOperation