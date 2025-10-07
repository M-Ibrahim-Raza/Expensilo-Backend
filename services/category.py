from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Category
from fastapi import HTTPException, status
from schemas.category import CategoriesReadResponse


def read_categories(db: Session) -> CategoriesReadResponse:

    categories = db.scalars(select(Category)).all()

    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories found",
        )

    return CategoriesReadResponse(categories=categories)


def read_category_users(db: Session, category_name: str) -> list[int]:

    category = db.query(Category).filter(Category.name == category_name).first()

    if not category:
        return []

    user_ids: list[int] = [uc.user_id for uc in category.users]

    return user_ids


def get_or_create_category(db: Session, category_name: str) -> int:

    existing_category = db.scalar(
        select(Category).where(Category.name == category_name)
    )

    if existing_category:
        return existing_category.id

    new_category = Category(name=category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category.id


def get_category_id(db: Session, category_name: str) -> str:

    category = db.scalar(select(Category).where(Category.name == category_name))

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_name} not found",
        )

    return category.id


def get_category_name(db: Session, category_id: int) -> str:

    category: Category = db.get(Category, category_id)

    return category.name
