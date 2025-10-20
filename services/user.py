from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db import add_commit_refresh

from models import User
from schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from auth import get_password_hash, verify_password


def get_user(db: Session, user_id: int) -> Optional[User]:

    user: Optional[User] = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:

    user: User | None = User.get_one(db, email=email)

    if not user:
        return "Incorrect email"

    if not verify_password(password, user.hashed_password):
        return "Incorrect password"

    return user


def read_user(db: Session, user_id: int) -> UserResponse:

    user = get_user(db=db, user_id=user_id)

    return UserResponse.model_validate(user)


def create_user(db: Session, user_create_request: UserCreateRequest) -> UserResponse:

    is_email_exist = User.get_one(db, email=user_create_request.email)

    if is_email_exist:
        return "Email already exist"

    new_user_data = user_create_request.model_dump()

    if new_user_data["password"]:
        del new_user_data["password"]

    if user_create_request.password:
        new_user_data["hashed_password"] = get_password_hash(
            user_create_request.password
        )

    new_user: User = User(**new_user_data)

    add_commit_refresh(db, new_user)

    return UserResponse.model_validate(new_user)


def delete_user(db: Session, user_id: int) -> UserResponse:

    user: User | None = get_user(db=db, user_id=user_id)

    deleted_user = UserResponse.model_validate(user)

    db.delete(user)
    db.commit()

    return deleted_user


def update_user(
    db: Session, user_id: int, user_update_request: UserUpdateRequest
) -> UserResponse:

    user: User | None = get_user(db=db, user_id=user_id)

    update_data = user_update_request.model_dump(exclude_unset=True, exclude_none=True)

    if update_data.get("password"):
        del update_data["password"]

    if user_update_request.password:
        update_data["hashed_password"] = get_password_hash(user_update_request.password)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return UserResponse.model_validate(user)
