from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import add_commit_refresh

from models import Transaction, UserTransaction
from schemas.transaction import TransactionBase
from schemas.user_transaction import (
    UserTransactionResponse,
    UserTransactionRequest,
    UserTransactionCreate,
    UserTransactionsResponse,
    UserTransactionUpdateRequest,
)
from services.category import get_category_id
from services.transaction import get_or_create_transaction
from services.user import get_user


def read_user_transactions(db: Session, user_id: int) -> UserTransactionsResponse:

    user = get_user(db=db, user_id=user_id)

    transactions: UserTransactionsResponse = UserTransactionsResponse(
        transactions=[
            UserTransactionResponse.from_orm_obj(transactions)
            for transactions in user.transactions
        ]
    )

    return transactions


def add_user_transaction(
    db: Session, user_id: int, user_transaction_request: UserTransactionRequest
) -> UserTransactionResponse:

    category_id: int = get_category_id(
        db=db, category_name=user_transaction_request.category
    )

    transaction: TransactionBase = TransactionBase(
        category_id=category_id,
        **user_transaction_request.model_dump(include={"type", "title"}),
    )

    transaction_id = get_or_create_transaction(db=db, transaction=transaction)

    user_transaction_create: UserTransactionCreate = UserTransactionCreate(
        user_id=user_id,
        transaction_id=transaction_id,
        **user_transaction_request.model_dump(
            include={"amount", "details", "attachments"}
        ),
    )

    new_user_transaction = UserTransaction(**user_transaction_create.model_dump())

    add_commit_refresh(db, new_user_transaction)

    user_transaction_response: UserTransactionResponse = (
        UserTransactionResponse.from_orm_obj(new_user_transaction)
    )

    return user_transaction_response


def delete_user_transaction(
    db: Session, user_id: int, user_transaction_id: int
) -> UserTransactionResponse:

    user = get_user(db=db, user_id=user_id)

    user_transaction_to_delete: UserTransaction | None = None
    for user_transaction in user.transactions:
        if user_transaction.id == user_transaction_id:
            user_transaction_to_delete = user_transaction
            break

    if not user_transaction_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction not found for user with id {user_id}",
        )

    transaction: Transaction = user_transaction_to_delete.transaction

    deleted_user_transaction: UserTransactionResponse = (
        UserTransactionResponse.from_orm_obj(user_transaction_to_delete)
    )

    db.delete(user_transaction_to_delete)
    db.flush()

    db.refresh(transaction)

    if not transaction.users:
        db.delete(transaction)

    db.commit()

    return deleted_user_transaction


def update_user_transaction(
    db: Session,
    user_id: int,
    user_transaction_id: int,
    user_transaction_update_request: UserTransactionUpdateRequest,
) -> UserTransactionResponse:

    user = get_user(db=db, user_id=user_id)

    user_transaction_to_update: UserTransaction | None = None
    for user_transaction in user.transactions:
        if user_transaction.id == user_transaction_id:
            user_transaction_to_update = user_transaction
            break

    if not user_transaction_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction not found for user with id {user_id}",
        )

    data = user_transaction_update_request.model_dump(
        exclude_unset=True, exclude_none=True
    )

    if "amount" in data:
        user_transaction_to_update.amount = Decimal(data["amount"])

    if "details" in data:
        user_transaction_to_update.details = data["details"]

    if "attachments" in data:
        user_transaction_to_update.attachments = data["attachments"]

    if "category" in data:
        category_id = get_category_id(data["category"])
        user_transaction_to_update.transaction.category_id = category_id

    if "type" in data:
        user_transaction_to_update.transaction.type = data["type"]

    if "title" in data:
        user_transaction_to_update.transaction.title = data["title"]

    db.commit()
    db.refresh(user_transaction_to_update)

    return UserTransactionResponse.from_orm_obj(user_transaction_to_update)
