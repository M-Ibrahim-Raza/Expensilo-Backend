from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from db import add_commit_refresh

from models import Category
from schemas.category import CategoriesResponse


def read_categories(db: Session) -> CategoriesResponse:

    categories = Category.get_all(db)

    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories found",
        )

    return CategoriesResponse(categories=categories)


def read_category_users(db: Session, category_name: str) -> list[int]:

    category = Category.get_one(db, name=category_name)

    if not category:
        return []

    user_ids: list[int] = [uc.user_id for uc in category.users]

    return user_ids


def get_or_create_category(db: Session, category_name: str) -> int:

    existing_category = Category.get_one(db, name=category_name)

    if existing_category:
        return existing_category.id

    new_category = Category(name=category_name)

    add_commit_refresh(db, new_category)

    return new_category.id


def get_category_id(db: Session, category_name: str) -> str:

    category = Category.get_one(db, name=category_name)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_name} not found",
        )

    return category.id
