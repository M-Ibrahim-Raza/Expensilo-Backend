from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db import add_commit_refresh

from models import User
from schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest


def get_user(db: Session, user_id: int) -> Optional[User]:

    user: Optional[User] = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return user


def read_user(db: Session, user_id: int) -> UserResponse:

    user = get_user(db=db, user_id=user_id)

    return UserResponse.model_validate(user)


def create_user(db: Session, user_create_request: UserCreateRequest) -> UserResponse:

    new_user: User = User(**user_create_request.model_dump())

    add_commit_refresh(db, new_user)

    return UserResponse.model_validate(new_user)


def delete_user(db: Session, user_id: int) -> UserResponse:

    user: User = get_user(db=db, user_id=user_id)

    deleted_user = UserResponse.model_validate(user)

    db.delete(user)
    db.commit()

    return deleted_user


def update_user(
    db: Session, user_id: int, user_update_request: UserUpdateRequest
) -> UserResponse:

    user = get_user(db=db, user_id=user_id)

    update_data = user_update_request.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return UserResponse.model_validate(user)
