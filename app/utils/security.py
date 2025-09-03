from passlib.context import CryptContext
from jose import JWTError, jwt 
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os


load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in environment variables")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = 60 * 24 * 7  
REFRESH_TOKEN_EXPIRATION = 30  

print(f"JWT Configuration - Algorithm: {ALGORITHM}, "
      f"Access Exp: {ACCESS_TOKEN_EXPIRATION} min, "
      f"Refresh Exp: {REFRESH_TOKEN_EXPIRATION} days")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


########PASSWD FUNC#############

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



###########JWT FUNC###########

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.now(timezone.utc)  
    })
    print(f"Creating access token that expires at (UTC): {expire}")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Generated token (first 30 chars): {str(encoded_jwt)[:30]}...")
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        print(f"Current UTC time: {datetime.now(timezone.utc)}")
        print(f"Decoding token: {token[:30]}...")
        
        # Decode without verification first to check expiration
        unverified = jwt.get_unverified_claims(token)
        print(f"Unverified token claims: {unverified}")
        
        if 'exp' in unverified:
            exp_time = datetime.fromtimestamp(unverified['exp'], tz=timezone.utc)
            print(f"Token expires at (UTC): {exp_time}")
            time_remaining = exp_time - datetime.now(timezone.utc)
            print(f"Time remaining: {time_remaining}")
        
        # Now verify and decode
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "verify_exp": True,
                "leeway": 10 
            }
        )
        print(f"Successfully decoded token. Payload: {payload}")
        return payload
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        if 'exp' in locals().get('unverified', {}):
            print(f"Token expired at: {datetime.fromtimestamp(unverified['exp'], tz=timezone.utc)}")
        return None