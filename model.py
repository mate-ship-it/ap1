from pydantic import BaseModel
from controller import Controller
from datetime import date, datetime

controller = Controller()

class AdmissionModel(BaseModel):
    adm_id: int
    adm_date_adm: date
    adm_pat_id: int
    adm_dist_id_a: str
    adm_date_dis: date
    adm_out_dis_id_a: int
    dis_id_a: int
    dis_desc: str

class PatientsModel(BaseModel):
    pat_id: int
    pat_fname: str
    pat_sname: str
    pat_address: str
    pat_city: str

class User(BaseModel):
    id: int
    email: str
    hashed_password: str
    role: str 
    created_at: datetime

class SignUp(BaseModel):
    email: str
    password: str

class SignIn(BaseModel):
    email: str
    password: str
    


    
    