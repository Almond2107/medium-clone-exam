from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- Auth schemas ---

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Response schemas ---

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_verified: bool
    created_at: datetime


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None



#####Token REsponse########
class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
