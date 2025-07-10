import os 
from dotenv import load_dotenv
from controller import Controller
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from model import AdmissionModel, PatientsModel, SignUp, SignIn
from auth import AuthHandler
from authorisation import allow_admissions_access, allow_patients_access
from auth import auth_handler

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
if not SECRET_KEY or not isinstance(SECRET_KEY, str):
    raise RuntimeError("SECRET_KEY is missing or invalid. Check your .env file.")

auth_handler = AuthHandler(SECRET_KEY, ALGORITHM)
controller = Controller()
router = APIRouter()

@router.get("/admissions", response_model=List[AdmissionModel])
def get_admissions(field=None, value=None, user = Depends(allow_admissions_access)):
    if field and value:
        return controller.get_filtered("admissions", field, value)
    else:
        return controller.get_all("admissions")

@router.get("/patients", response_model=List[PatientsModel])
def get_patients(field=None, value=None, user = Depends(allow_patients_access)):
    if field and value:
        return controller.get_filtered("patients", field, value)
    else:
        return controller.get_all("patients")
    
@router.post("/signup", response_model=dict)
def signup(user:SignUp):
    if user.email.endswith("@fastapi.com"):
        hashed_pwd = auth_handler.get_password_hash(user.password)
        controller.insert_admin_in_db(user.email, hashed_pwd)
    else:
        hashed_pwd = auth_handler.get_password_hash(user.password)
        controller.insert_user(user.email, hashed_pwd)
    return {"message": "Successful Registration"}

@router.post("/login", response_model=dict)
def login(user:SignIn):
    from_db = controller.get_user(user.email)
    if from_db is None or from_db.empty:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    hashed_pw = from_db["hashed_password"][0]
    if not auth_handler.verify_password(user.password, hashed_pw):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    token = auth_handler.create_access_token({"sub": user.email, "role": from_db["role"][0]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/whoami")
def identity(user_email = Depends(auth_handler.decode_access_token)):
    return {"email": user_email}