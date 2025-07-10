from urllib import response as resp
from database import Database

database_service = Database()

class Controller:
    def __init__(self):
        self.database = database_service

    def get_all(self, source):
        df = getattr(self.database, f"{source}_data")
        return df.to_dict(orient="records")
    
    def insert_user(self, email, hash_password, role='user'):
        user_df = self.database.user_data
        if email in user_df["email"].values:
            raise ValueError("Email is already Registered")
        else:
            self.database.insert_user_to_db(email, hash_password, role)    
            
        return ("User has been successfully registered")
    
    def insert_admin_in_db(self, email, hash_password, role='admin'):
        if email.endswith("@fastapi.com"):
            self.database.insert_user_to_db(email, hash_password, role)
        else:
            raise ValueError("Registered as User")

    def get_user(self, email):
        return self.database.get_user_in_db(email)

    def get_filtered(self, source, field, value):
        df = getattr(self.database, f"{source}_data")
        
        if field is not None:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
            df = df[df[field] == value]

        return df.to_dict(orient="records")

        