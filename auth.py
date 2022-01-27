from tkinter.font import names
from config_db import Users, db

class User():
    def __init__(self, username, userpassword):
        self.name = username
        self.password = userpassword

    def auth_user(self):
        user = Users.query.filter_by(user_name=self.name, user_pass=self.password).first()
        if user != None:
            return True
        else:
            return False

