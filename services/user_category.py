from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import select
from schemas.user_category import UserCategoryResponse
from schemas.category import CategoriesReadResponse
from services.category import get_or_create_category
from services.user import get_user
from models import UserCategory


def read_user_categories(db: Session, user_id: int) -> CategoriesReadResponse:

    user = get_user(db=db, user_id=user_id)

    categories: CategoriesReadResponse = CategoriesReadResponse(
        categories=[uc.category for uc in user.categories]
    )
    return categories


def add_user_category(
    db: Session, user_id: int, category_name: str
) -> UserCategoryResponse:

    category_id: int = get_or_create_category(db=db, category_name=category_name)

    existing_link = db.scalar(
        select(UserCategory).where(
            UserCategory.user_id == user_id,
            UserCategory.category_id == category_id,
        )
    )

    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category '{category_name}' is already linked to this user.",
        )

    new_user_category = UserCategory(user_id=user_id, category_id=category_id)
    db.add(new_user_category)
    db.commit()
    db.refresh(new_user_category)

    return UserCategoryResponse.model_validate(new_user_category)


def delete_user_category(db: Session, user_id: int, category_name: str):

    user = get_user(db=db, user_id=user_id)

    user_category_to_delete = None
    for user_category in user.categories:
        if user_category.category.name == category_name:
            user_category_to_delete = user_category
            break

    if not user_category_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category '{category_name}' not linked to user with id {user_id}",
        )

    category = user_category_to_delete.category

    db.delete(user_category_to_delete)

    if not category.users:
        db.delete(category)

    db.commit()
