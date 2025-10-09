from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session

from db.db_setup import get_db_session
from schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from services.user import create_user, read_user, update_user, delete_user
from auth import get_current_user_id

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get details of exsiting user",
    response_description="The details of user",
)
def get_user_endpoint(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> UserResponse:

    user: UserResponse = read_user(db=db, user_id=user_id)
    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The newly created user",
)
def create_user_endpoint(
    user_create_request: UserCreateRequest,
    db: Session = Depends(get_db_session),
) -> UserResponse:

    user: UserResponse = create_user(db=db, user_create_request=user_create_request)
    return user


@router.delete(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete existing user",
    response_description="The details of deleted user",
)
def delete_user_endpoint(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> UserResponse:
    user: UserResponse = delete_user(db=db, user_id=user_id)
    return user


@router.put(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Update details of existing user",
    response_description="The updated details of user",
)
def update_user_endpoint(
    user_update_request: UserUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
) -> UserResponse:
    user: UserResponse = update_user(
        db=db, user_id=user_id, user_update_request=user_update_request
    )
    return user
