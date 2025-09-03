from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.dependencies import db_dep, current_user_dep
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(user: current_user_dep):
    return user


@router.put("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    db: db_dep,
    current_user: current_user_dep,
):
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    db: db_dep,
    current_user: current_user_dep,
):
    db.delete(current_user)
    db.commit()
    return None
