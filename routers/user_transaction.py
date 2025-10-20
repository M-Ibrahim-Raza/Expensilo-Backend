from typing import Annotated

from fastapi import APIRouter, status, Path, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from db import get_db_session
from schemas.user_transaction import (
    UserTransactionRequest,
    UserTransactionResponse,
    UserTransactionsResponse,
    UserTransactionUpdateRequest,
    ExportRequest,
)
from services.user_transaction import (
    add_user_transaction,
    read_user_transactions,
    delete_user_transaction,
    update_user_transaction,
    generate_CSV,
    generate_PDF,
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


@router.post(
    "/export-csv",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"content": {"text/csv": {}}},
        404: {"description": "File not found"},
    },
    summary="Download the transactions CSV file",
    response_description="Returns a CSV file containing exported transactions.",
)
def export_csv_endpoint(transactions: ExportRequest):
    file_path = generate_CSV(data=transactions)

    return FileResponse(
        path=file_path,
        status_code=status.HTTP_200_OK,
        media_type="text/csv",
        filename="transactions.csv",
        headers={"Content-Disposition": f'attachment; filename="transactions.csv"'},
    )


@router.post(
    "/export-pdf",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"content": {"application/pdf": {}}},
        404: {"description": "File not found"},
    },
    summary="Download the transactions PDF file",
    response_description="Returns a PDF file containing exported transactions.",
)
def export_pdf_endpoint(transactions: ExportRequest):

    file_path = generate_PDF(data=transactions)

    return FileResponse(
        path=file_path,
        status_code=status.HTTP_200_OK,
        media_type="application/pdf",
        filename="transactions.pdf",
        headers={"Content-Disposition": f'attachment; filename="transactions.pdf"'},
    )
