# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenData
from app.models.user import User
from app.utils.security import (
    hash_password, verify_password, create_access_token, create_refresh_token
)
from app.utils.dependencies import db_dep, current_user_dep, get_db
from uuid import uuid4
from fastapi.security import OAuth2PasswordRequestForm
from app.settings import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: db_dep):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_pw,
        is_active=True,
        is_verified=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

#send email veryfy link
    token = str(uuid4())  
    
    return new_user





@router.post("/login", response_model=TokenData)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print(f"Login attempt for user: {form_data.username}")  # Debug log
    
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        print("User not found")  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    print(f"User found: {user.email}")
    
    if not verify_password(form_data.password, user.password_hash):
        print("Invalid password")  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})
        
        print(f"Tokens generated successfully for {user.email}")  
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        print(f"Error generating tokens: {str(e)}")  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating authentication tokens"
        )



@router.get("/me", response_model=UserResponse)
def get_me(user: current_user_dep):
    return user




@router.post("/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_verified = True
            db.commit()
            return {"message": "Email verified"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
