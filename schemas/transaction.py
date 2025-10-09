from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from enums import TransactionType


class TransactionBase(BaseModel):

    category_id: Annotated[
        int|None,
        Field(
            None,
            title="Category ID",
            description="The unique ID of the category",
            example=1,
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


class TransactionRead(TransactionBase):

    id: Annotated[
        int,
        Field(
            ...,
            title="Transaction ID",
            description="The unique ID of the transaction",
            example=1,
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


class TransactionsResponse(BaseModel):

    transactions: Annotated[
        list[TransactionRead],
        Field(title="Transaction List", description="The list of all the transaction"),
    ]

    model_config = ConfigDict(from_attributes=True)
