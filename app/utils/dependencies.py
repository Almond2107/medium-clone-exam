from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import decode_token
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

#######OAuth2 token bearer schema############

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


#####Database Session dependency######

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dep = Annotated[Session, Depends(get_db)]
oauth2_scheme_dep = Annotated[str, Depends(oauth2_scheme)]


####### Current user extractor ########

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    print(f"Validating token: {token}")  
    
    try:
        payload = decode_token(token)
        print(f"Decoded payload: {payload}")  
        
        if not payload or "sub" not in payload:
            print("No 'sub' in payload")  
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        email = payload.get("sub")
        print(f"Looking for user with email: {email}") 
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print("User not found in database")  
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        print(f"User authenticated: {user.email}")  
        return user
        
    except JWTError as e:
        print(f"JWT validation error: {str(e)}")  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


#### This is Optional shortcut for current user #####

current_user_dep = Annotated[User, Depends(get_current_user)]