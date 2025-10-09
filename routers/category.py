from typing import Annotated

from fastapi import APIRouter, status, Depends, Path

from db import get_db_session
from schemas.category import CategoriesResponse
from services.category import read_categories, read_category_users


router = APIRouter(prefix="/category", tags=["Category"])


@router.get(
    "",
    response_model=CategoriesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all categories",
    response_description="The list of all categories",
)
def get_categories_endpoint(db=Depends(get_db_session)) -> CategoriesResponse:
    categories: CategoriesResponse = read_categories(db=db)
    return categories


@router.get(
    "/{category_name}/users",
    response_model=list[int],
    status_code=status.HTTP_200_OK,
    summary="Get all users of a category",
    response_description="The list of IDs of all users having this category",
)
def get_category_users_endpoint(
    category_name: Annotated[
        str, Path(..., title="Category Name", description="Name of the Category")
    ],
    db=Depends(get_db_session),
):
    category_users: list[int] = read_category_users(db=db, category_name=category_name)
    return category_users
