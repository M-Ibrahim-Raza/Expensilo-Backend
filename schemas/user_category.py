from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class UserCategoryRequest(BaseModel):
    category_name: Annotated[
        str,
        Field(
            ...,
            title="Category Name",
            description="Name of the category",
            example="Rent",
        ),
    ]


class UserCategoryResponse(BaseModel):
    user_id: Annotated[
        int, Field(..., title="User ID", description="ID of the user", example=1)
    ]

    category_id: Annotated[
        int,
        Field(..., title="Category ID", description="ID of the category", example=1),
    ]

    model_config = ConfigDict(from_attributes=True)
