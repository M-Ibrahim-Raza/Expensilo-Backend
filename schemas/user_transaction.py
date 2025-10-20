from typing import Annotated, Optional, Type
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from enums import TransactionType
from models import UserTransaction


class UserTranactionBase(BaseModel):

    amount: Annotated[
        Decimal,
        Field(
            ...,
            title="Transaction Amount",
            description="Amount of transaction with up to 2 decimal places",
            example="1500.50",
        ),
    ]

    details: Annotated[
        Optional[str],
        Field(
            None,
            title="Details",
            description="Additional transaction details or notes",
            example="Monthly rent payment",
        ),
    ]

    attachments: Annotated[
        Optional[list[str]],
        Field(
            None,
            title="Attachments",
            description="List of file names or URLs associated with the transaction",
            example=["receipt1.png", "invoice.pdf"],
        ),
    ]

    created_at: Annotated[
        datetime | None,
        Field(
            None,
            title="Created At",
            description="Timestamp when the transaction was created",
            example="2025-10-07T12:30:00Z",
        ),
    ]


class UserTransactionCreate(UserTranactionBase):

    user_id: Annotated[
        int,
        Field(
            ...,
            title="User ID",
            description="Unique ID of the user",
            example=1,
        ),
    ]

    transaction_id: Annotated[
        int,
        Field(
            ...,
            title="User ID",
            description="Unique ID of the user",
            example=1,
        ),
    ]


class UserTransactionRequest(UserTranactionBase):

    category: Annotated[
        str | None,
        Field(
            None,
            title="Category Name",
            description="The unique name of the category",
            example="Rent",
        ),
    ]

    type: Annotated[
        TransactionType,
        Field(
            ...,
            title="Transaction type",
            description="Transaction type: EXPENSE or INCOME",
        ),
    ]

    title: Annotated[
        str, Field(..., title="Transaction Title", description="Title of transaction")
    ]


class UserTransactionResponse(UserTransactionRequest):

    id: Annotated[
        int,
        Field(
            ...,
            title="User Transaction ID",
            description="Unique ID of the user transaction",
            example=1,
        ),
    ]

    user_id: Annotated[
        int,
        Field(
            ...,
            title="User ID",
            description="Unique ID of the user",
            example=1,
        ),
    ]

    created_at: Annotated[
        datetime,
        Field(
            ...,
            title="Created At",
            description="Timestamp when the transaction was created",
            example="2025-10-07T12:30:00Z",
        ),
    ]

    updated_at: Annotated[
        datetime,
        Field(
            ...,
            title="Updated At",
            description="Timestamp when the transaction was last updated",
            example="2025-10-07T13:00:00Z",
        ),
    ]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_obj(
        cls: Type["UserTransactionResponse"], obj: "UserTransaction"
    ) -> "UserTransactionResponse":

        return cls(
            id=obj.id,
            user_id=obj.user_id,
            amount=obj.amount,
            details=obj.details,
            attachments=obj.attachments,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            category=(
                obj.transaction.category.name if obj.transaction.category else None
            ),
            type=obj.transaction.type if obj.transaction else None,
            title=obj.transaction.title if obj.transaction else None,
        )


class UserTransactionsResponse(BaseModel):

    transactions: Annotated[
        list[UserTransactionResponse],
        Field(
            ...,
            title="User Transaction List",
            description="List of transactions of a user",
        ),
    ]


class UserTransactionUpdateRequest(BaseModel):

    amount: Annotated[
        Decimal | None,
        Field(
            None,
            title="Transaction Amount",
            description="Amount of transaction with up to 2 decimal places",
            example="1500.50",
        ),
    ]

    details: Annotated[
        str | None,
        Field(
            None,
            title="Details",
            description="Additional transaction details or notes",
            example="Monthly rent payment",
        ),
    ]

    attachments: Annotated[
        list[str] | None,
        Field(
            None,
            title="Attachments",
            description="List of file names or URLs associated with the transaction",
            example=["receipt1.png", "invoice.pdf"],
        ),
    ]

    category: Annotated[
        str | None,
        Field(
            None,
            title="Category Name",
            description="The unique name of the category",
            example="Rent",
        ),
    ]

    created_at: Annotated[
        datetime | None,
        Field(
            None,
            title="Created At",
            description="Timestamp when the transaction was created",
            example="2025-10-07T12:30:00Z",
        ),
    ]

    type: Annotated[
        TransactionType | None,
        Field(
            None,
            title="Transaction type",
            description="Transaction type: EXPENSE or INCOME",
        ),
    ]

    title: Annotated[
        str | None,
        Field(None, title="Transaction Title", description="Title of transaction"),
    ]


class ExportRequest(BaseModel):

    transactions: Annotated[
        list[UserTransactionResponse],
        Field(
            ...,
            title="User Transaction List",
            description="List of transactions of a user",
        ),
    ]
