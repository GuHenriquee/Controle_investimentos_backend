from fastapi import APIRouter, Depends
from objects.operationOB import Operation, OperationInDB, OperationResponse
from objects.userOB import UserInDB
from funcionalities.APIs.database import database
from funcionalities.requestsFuncs.operations import Operations
from typing import Annotated
from funcionalities.requestsFuncs.loginFuncs import LoginAndJWT

router = APIRouter()

@router.post("/api/operation/", status_code=201)
def operator(operation: Operation, session: database.SessionDep, 
             current_user: Annotated[UserInDB, Depends(LoginAndJWT.get_current_active_user)])-> OperationResponse:
    

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