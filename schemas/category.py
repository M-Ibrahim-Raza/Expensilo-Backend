from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


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


class CategoriesResponse(BaseModel):

    categories: Annotated[
        list[CategoryRead],
        Field(title="Categories List", description="The list of all the categories"),
    ]

    model_config = ConfigDict(from_attributes=True)
