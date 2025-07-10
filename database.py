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
    

        