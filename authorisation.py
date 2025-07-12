from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import auth_handler

# Define the security scheme for Swagger and FastAPI
security = HTTPBearer()

# Authorization Gatekeepers
def allow_admissions_access(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials  # Extract the raw JWT token
    email, role = auth_handler.decode_access_token(token)  # Validate and decode token
    if role in ["user", "admin"]:
        return email
    else:
        raise HTTPException(status_code=403, detail="User Unauthorised")

def allow_patients_access(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    email, role = auth_handler.decode_access_token(token)
    if role == "admin":
        return email
    else:
        raise HTTPException(status_code=403, detail="User Unauthorised")
