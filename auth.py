from jose import jwt, JWTError
from keymanager import KeyManager
from passlib.context import CryptContext
from fastapi import HTTPException, Request
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
    
    def create_access_token(self, data:dict, expires_delta: Optional[timedelta]=None):
        to_encode = data.copy()

        if expires_delta:
            to_encode["exp"] = (datetime.now(timezone.utc) + expires_delta)
            to_encode["exp"]
        else:
            to_encode["exp"] = datetime.now(timezone.utc) +  timedelta(minutes=30)
            to_encode["exp"]
            
        token = jwt.encode(to_encode, key_manager.get_active_key(), self.algorithm)
        return token 

    def decode_access_token(self, token):
        auth_header = request.headers.get("authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

        token = auth_header.split(" ")[1]
        
        valid_keys = key_manager.get_valid_keys()

        for key in key_manager.get_valid_keys():
            try:
                decode_token = jwt.decode(token, key, algorithms=[self.algorithm])
                sub = decode_token["sub"]
                role = decode_token["role"]
                return sub, role
            
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expired")
            except JWTError:
                pass
                
        raise HTTPException(status_code=401, detail="Invalid token format")

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

auth_handler = AuthHandler(ALGORITHM)
        
