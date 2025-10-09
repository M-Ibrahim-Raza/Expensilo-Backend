from typing import Annotated

from fastapi import APIRouter, status, Path, Depends
from sqlalchemy.orm import Session

from db import get_db_session
from schemas.category import CategoriesResponse
from schemas.user_category import UserCategoryRequest, UserCategoryResponse
from services.user_category import (
    add_user_category,
    read_user_categories,
    delete_user_category,
)
from auth import get_current_user_id

router = APIRouter(prefix="/users/category", tags=["Users Category"])


@router.get(
    "",
    response_model=CategoriesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user categories",
    response_description="List of categories names",
)
def get_user_categories_endpoint(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> CategoriesResponse:

    categories: CategoriesResponse = read_user_categories(db=db, user_id=user_id)

    return categories


@router.post(
    "",
    response_model=UserCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create user category",
    response_description="IDs of user and category",
)
def add_user_category_endpoint(
    user_category_request: UserCategoryRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> UserCategoryResponse:

    user_category_response: UserCategoryResponse = add_user_category(
        db=db, user_id=user_id, category_name=user_category_request.category_name
    )

    return user_category_response


@router.delete(
    "/{category_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user category",
)
def delete_user_category_endpoint(
    category_name: Annotated[
        str, Path(..., title="Category Name", description="Name of the Category")
    ],
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> None:

    delete_user_category(db=db, user_id=user_id, category_name=category_name)
