from fastapi import APIRouter, status, Depends

from db import get_db_session
from schemas.transaction import TransactionsResponse
from services.transaction import read_transactions


router = APIRouter(prefix="/transaction", tags=["Transaction"])


@router.get(
    "",
    response_model=TransactionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all transactions",
    response_description="The list of all transactions",
)
def get_transactions_endpoint(db=Depends(get_db_session)) -> TransactionsResponse:
    transactions: TransactionsResponse = read_transactions(db=db)
    return transactions
