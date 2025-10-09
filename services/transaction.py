from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from db import add_commit_refresh

from models import Transaction
from schemas.transaction import TransactionsResponse, TransactionBase


def read_transactions(db: Session) -> TransactionsResponse:

    transactions = Transaction.get_all(db)

    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No transactions found",
        )

    return TransactionsResponse(transactions=list(transactions))


def get_or_create_transaction(db: Session, transaction: TransactionBase) -> int:

    existing_transaction = Transaction.get_one(
        db,
        type=transaction.type,
        title=transaction.title,
        category_id=transaction.category_id,
    )

    if existing_transaction:
        return existing_transaction.id

    new_transaction = Transaction(**transaction.model_dump())

    add_commit_refresh(db, new_transaction)

    return new_transaction.id
