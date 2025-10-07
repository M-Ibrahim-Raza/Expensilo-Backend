from sqlalchemy.orm import Session
from schemas.transaction import TransactionsReadResponse, TransactionBase
from sqlalchemy import select
from models import Transaction
from fastapi import HTTPException, status


def read_transactions(db: Session) -> TransactionsReadResponse:

    transactions = db.scalars(select(Transaction)).all()

    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No transactions found",
        )

    return TransactionsReadResponse(transactions=transactions)


def get_or_create_transaction(db: Session, transaction: TransactionBase) -> int:

    existing_transaction = db.scalar(
        select(Transaction).where(
            Transaction.type == transaction.type,
            Transaction.title == transaction.title,
            Transaction.category_id == transaction.category_id,
        )
    )

    if existing_transaction:
        return existing_transaction.id

    new_transaction = Transaction(**transaction.model_dump())

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction.id
