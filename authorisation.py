from fastapi import Depends, HTTPException
from auth import auth_handler

 # Authorization Gatekeepers
def allow_admissions_access(user = Depends(auth_handler.decode_access_token)):
    email, role = user
    if role in ["user", "admin"]:
        return email
    else:
        raise HTTPException(status_code=403, detail="User Unauthorised")

def allow_patients_access(user = Depends(auth_handler.decode_access_token)):
    email, role = user
    if role == "admin":
        return email
    else:
        raise HTTPException(status_code=403, detail="User Unauthorised")