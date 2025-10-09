from typing import Annotated

from fastapi import APIRouter, status, Path, Depends
from sqlalchemy.orm import Session

from db import get_db_session
from schemas.user_transaction import (
    UserTransactionRequest,
    UserTransactionResponse,
    UserTransactionsResponse,
    UserTransactionUpdateRequest,
)
from services.user_transaction import (
    add_user_transaction,
    read_user_transactions,
    delete_user_transaction,
    update_user_transaction,
)
from auth import get_current_user_id

router = APIRouter(prefix="/users/transaction", tags=["Users Transaction"])


@router.get(
    "",
    response_model=UserTransactionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user transactions",
    response_description="List of transactions of a user",
)
def get_user_transactions_endpoint(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> UserTransactionsResponse:

    transactions: UserTransactionsResponse = read_user_transactions(
        db=db, user_id=user_id
    )

    return transactions


@router.post(
    "",
    response_model=UserTransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create user transaction",
    response_description="Details of user transaction",
)
def add_user_transaction_endpoint(
    user_transaction_request: UserTransactionRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> UserTransactionResponse:

    print(user_transaction_request)

    user_transaction_response: UserTransactionRequest = add_user_transaction(
        db=db, user_id=user_id, user_transaction_request=user_transaction_request
    )

    return user_transaction_response


@router.put(
    "/{user_transaction_id}",
    response_model=UserTransactionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Updates user transaction",
)
def update_user_transaction_endpoint(
    user_transaction_id: Annotated[
        int,
        Path(
            ..., title="Transaction ID", description="Unique ID of the user transaction"
        ),
    ],
    user_transaction_update_request: UserTransactionUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> UserTransactionResponse:

    updated_user_transaction: UserTransactionResponse = update_user_transaction(
        db=db,
        user_id=user_id,
        user_transaction_id=user_transaction_id,
        user_transaction_update_request=user_transaction_update_request,
    )

    return updated_user_transaction


@router.delete(
    "/{user_transaction_id}",
    response_model=UserTransactionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete user transaction",
)
def delete_user_transaction_endpoint(
    user_transaction_id: Annotated[
        int,
        Path(
            ..., title="Transaction ID", description="Unique ID of the user transaction"
        ),
    ],
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> UserTransactionResponse:

    deleted_user_transaction: UserTransactionResponse = delete_user_transaction(
        db=db, user_id=user_id, user_transaction_id=user_transaction_id
    )

    return deleted_user_transaction
