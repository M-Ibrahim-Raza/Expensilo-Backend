import os
import csv
from datetime import datetime
from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import add_commit_refresh

from models import Transaction, UserTransaction, UserCategory
from schemas.transaction import TransactionBase
from schemas.user_transaction import (
    UserTransactionResponse,
    UserTransactionRequest,
    UserTransactionCreate,
    UserTransactionsResponse,
    UserTransactionUpdateRequest,
    ExportRequest,
)
from services.category import get_or_create_category
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

    category_id: int = get_or_create_category(
        db=db, category_name=user_transaction_request.category
    )

    existing_link = UserCategory.get_one(db, user_id=user_id, category_id=category_id)

    if not existing_link:
        new_user_category = UserCategory(user_id=user_id, category_id=category_id)
        add_commit_refresh(db, new_user_category)

    transaction: TransactionBase = TransactionBase(
        category_id=category_id,
        **user_transaction_request.model_dump(include={"type", "title"}),
    )

    transaction_id = get_or_create_transaction(db=db, transaction=transaction)

    user_transaction_create: UserTransactionCreate = UserTransactionCreate(
        user_id=user_id,
        transaction_id=transaction_id,
        **user_transaction_request.model_dump(
            exclude_none=True,
            include={"amount", "details", "attachments", "created_at"},
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

    if "created_at" in data:
        user_transaction_to_update.created_at = data["created_at"]

    if "category" in data:
        category_id: int = get_or_create_category(db=db, category_name=data["category"])

        existing_link = UserCategory.get_one(
            db, user_id=user_id, category_id=category_id
        )

        if not existing_link:
            new_user_category = UserCategory(user_id=user_id, category_id=category_id)
            add_commit_refresh(db, new_user_category)

        user_transaction_to_update.transaction.category_id = category_id

    if "type" in data:
        user_transaction_to_update.transaction.type = data["type"]

    if "title" in data:
        user_transaction_to_update.transaction.title = data["title"]

    db.commit()
    db.refresh(user_transaction_to_update)

    return UserTransactionResponse.from_orm_obj(user_transaction_to_update)


def generate_CSV(data: ExportRequest):

    data = data.model_dump()

    folder_path = os.path.join(os.getcwd(), "temp")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "transactions.csv")

    transactions = data.get("transactions", [])

    headers = ["Type", "Title", "Amount", "Category", "Date"]

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for txn in transactions:
            txn_type = txn["type"].value
            title = txn["title"]
            amount = (
                float(txn["amount"])
                if isinstance(txn["amount"], Decimal)
                else txn["amount"]
            )
            category = txn["category"]
            date = (
                txn["created_at"].strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(txn["created_at"], datetime)
                else txn["created_at"]
            )

            writer.writerow([txn_type, title, amount, category, date])

    return file_path


def generate_PDF(data: ExportRequest):

    data = data.model_dump()

    folder_path = os.path.join(os.getcwd(), "temp")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "transactions.pdf")

    transactions = data.get("transactions", [])

    pdf = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("<b>Transaction Report</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    headers = ["Type", "Title", "Amount", "Category", "Date"]
    table_data = [headers]

    for txn in transactions:
        txn_type = txn["type"].value if hasattr(txn["type"], "value") else txn["type"]
        title = txn["title"]
        amount = (
            float(txn["amount"])
            if isinstance(txn["amount"], Decimal)
            else txn["amount"]
        )
        category = txn["category"]
        date = (
            txn["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(txn["created_at"], datetime)
            else txn["created_at"]
        )

        table_data.append([txn_type, title, f"{amount:.2f}", category, date])

    table = Table(
        table_data, colWidths=[1 * inch, 2 * inch, 1 * inch, 1.5 * inch, 2 * inch]
    )

    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]
    )
    table.setStyle(style)

    elements.append(table)
    pdf.build(elements)

    return file_path
