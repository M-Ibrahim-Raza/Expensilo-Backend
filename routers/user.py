from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from db.db_setup import get_db_session
from schemas.user import UserCreateRequest, UserReadResponse, UserUpdateRequest
from services.user import create_user, read_user, update_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Read details of exsiting user",
    response_description="The details of user",
)
def read_user_endpoint(
    user_id: Annotated[int, Path(...)], db: Session = Depends(get_db_session)
) -> UserReadResponse:

    user: UserReadResponse = read_user(db=db, user_id=user_id)
    return user


@router.post(
    "/",
    response_model=UserReadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The newly created user",
)
def create_user_endpoint(
    user_create_request: UserCreateRequest,
    db: Session = Depends(get_db_session),
) -> UserReadResponse:

    user: UserReadResponse = create_user(db=db, user=user_create_request)
    return user


@router.put(
    "/{user_id}",
    response_model=UserReadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Update details of existing user",
    response_description="The updated details of user",
)
def update_user_endpoint(
    user_id: Annotated[int, Path(...)],
    user_update_request: UserUpdateRequest,
    db: Session = Depends(get_db_session),
) -> UserReadResponse:
    user: UserReadResponse = update_user(
        db=db, user_id=user_id, user_update_request=user_update_request
    )
    return user


# @router.get("{user_id}/preferences")
