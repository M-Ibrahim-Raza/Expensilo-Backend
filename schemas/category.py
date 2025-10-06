from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class CategoryRead(BaseModel):
    id: Annotated[
        int,
        Field(
            ...,
            title="Category ID",
            description="The unique ID of the category",
            example=1,
        ),
    ]

    name: Annotated[
        str,
        Field(
            ...,
            title="Category Name",
            description="The unique name of the category",
            example="Rent",
        ),
    ]
    model_config = ConfigDict(from_attributes=True)


class CategoriesReadResponse(BaseModel):
    categories: Annotated[
        list[CategoryRead],
        Field(title="Categories List", description="The list of all the categories"),
    ]

    model_config = ConfigDict(from_attributes=True)
