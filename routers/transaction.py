from fastapi import APIRouter, status, Depends
from schemas.transaction import TransactionsReadResponse
from services.transaction import read_transactions
from db import get_db_session

router = APIRouter(prefix="/transaction", tags=["Transaction"])


@router.get(
    "",
    response_model=TransactionsReadResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all transactions",
    response_description="The list of all transactions",
)
def get_transactions_endpoint(db=Depends(get_db_session)) -> TransactionsReadResponse:
    transactions: TransactionsReadResponse = read_transactions(db=db)
    return transactions
