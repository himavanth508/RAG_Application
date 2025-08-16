from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from db import users_collection
from bson.objectid import ObjectId


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
print("oauth2_scheme:", oauth2_scheme)

def verify_password(plain_password, hashed):
    return pwd_context.verify(plain_password, hashed)

def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("get_current_user called with token:", token)
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        print("hsioihfosihf",token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)
        username = payload.get("sub")
        print("sefsfsfawsfa",username,payload)
        user = users_collection.find_one({"username": username})
        print("user found:", user)
        if not user:
            raise credentials_exception
        return user
    except JWTError as e:
        print("JWTError occurred", e)
        raise credentials_exception
