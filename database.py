import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import os 
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv("DB_URL")
if not db_url:
    raise ValueError("DB_URL is not set in the environment variables")

db = create_engine(db_url)

class Database():
    def __init__(self):
        self.admissions_data = pd.read_sql("SELECT * FROM admissions", db)
        self.patients_data = pd.read_sql("SELECT * FROM patients", db)
        self.user_data = pd.read_sql("SELECT * FROM users", db)
        self.patient_documents_data = pd.read_sql("SELECT * FROM patient_documents", db)

    def insert_user_to_db(self, email, hashed_password, role):
        with db.begin() as conn:
            query = text("""
                INSERT INTO users (email, hashed_password, role)
                VALUES (:email, :hashed_password, :role)
            """)
            conn.execute(query, {
                "email": email,
                "hashed_password": hashed_password,
                "role": role
            })

    def get_user_in_db(self, email):
        query = text("SELECT * FROM users WHERE email = :email")
        result = pd.read_sql(query, db, params={"email":email})
        return result 
    
    def insert_patient_document(self, pat_id, filename, filepath):
        with db.begin() as conn:
            query = text("""
                INSERT INTO patient_documents (pat_id, filename, filepath)
                VALUES (:pat_id, :filename, :filepath)
                         """)
            conn.execute(query, {
                "pat_id": pat_id,
                "filename": filename,
                "filepath": filepath
            })

    def get_documents_by_patient(self, pat_id):
        query = text("SELECT * FROM patient_documents WHERE pat_id = :pat_id")
        result = pd.read_sql(query, db, params={"pat_id": pat_id})
        return result
