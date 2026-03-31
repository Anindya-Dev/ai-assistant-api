from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from jose import JWTError
from dotenv import load_dotenv
from passlib.context import CryptContext
import os

load_dotenv()

security=HTTPBearer()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain:str, hashed:str):
    return pwd_context.verify(plain,hashed)

def create_access_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token= credentials.credentials

    payload=verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    
    return payload