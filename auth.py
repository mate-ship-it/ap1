from jose import jwt, JWTError
from keymanager import KeyManager
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import timezone, timedelta, datetime
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
key_manager = KeyManager()

class AuthHandler():
    def __init__(self, ALGORITHM):
        self.algorithm = ALGORITHM

    def get_password_hash(self, password):
        hashed = pwd_context.hash(password)
        return hashed

    def verify_password(self, plain, hashed):
        verified = pwd_context.verify(plain, hashed)
        if verified:
            return True
        else:
            raise ValueError("The password is wrong")
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        if expires_delta:
            to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
        else:
            to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=30)
            
        token = jwt.encode(to_encode, key_manager.get_active_key(), self.algorithm)
        return token

    def decode_access_token(self, token: str):
        valid_keys = key_manager.get_valid_keys()

        for key in valid_keys:
            try:
                decode_token = jwt.decode(token, key, algorithms=[self.algorithm])
                sub = decode_token.get("sub")
                role = decode_token.get("role")

                if not sub or not role:
                    raise HTTPException(status_code=401, detail="Token missing required claims")

                return sub, role
            
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expired")
            except JWTError:
                continue
                
        raise HTTPException(status_code=401, detail="Invalid token format")

# Load settings from .env
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

auth_handler = AuthHandler(ALGORITHM)
