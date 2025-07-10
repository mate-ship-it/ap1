from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import timezone, timedelta, datetime
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthHandler():
    def __init__(self, SECRET_KEY, ALGORITHM):
        self.secret = SECRET_KEY
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
            
        token = jwt.encode(to_encode,self.secret, self.algorithm)
        return token 

    def decode_access_token(self, token):
        auth_token = token

        try:
            decoded_token = jwt.decode(auth_token, self.secret, algorithms=[self.algorithm])
            sub = decoded_token["sub"]
            role = decoded_token["role"]
            return sub, role 

        except jwt.ExpiredSignatureError:
            print("Invalid Token")
            raise HTTPException(status_code=401, detail="Token expired")

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

auth_handler = AuthHandler(SECRET_KEY, ALGORITHM)
        
