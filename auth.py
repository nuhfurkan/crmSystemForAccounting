from tkinter.font import names
from config_db import CLientAccount, Company, Employee, ToVerify, Users, db, Client

class User():
    def __init__(self, username, userpassword):
        self.name = username
        self.password = userpassword
        self.id = None

    def auth_employee(self):
        thisUser = Users.query.filter_by(user_name=self.name, user_pass=self.password).first()
        if thisUser != None:
            employee = Employee.query.filter_by(user=thisUser.id).first()
            if employee != None:
                self.id = thisUser.id
                return thisUser.id
            else:
                return False
        else:
            return False
        
    def auth_client(self):
        thisUser = Users.query.filter_by(user_name=self.name, user_pass=self.password).first()
        if thisUser != None:
            client = CLientAccount.query.filter_by(User=thisUser.id).first()
            if client != None:
                self.id = thisUser.id
                return thisUser.id
            else:
                return False
        else:
            return False

def verificationComplete(email, verif_code, type, company):
    verif_user = ToVerify.query.filter_by(email=email, verification_code=verif_code).first()
    if verif_user != None:
        new_user = Users(firs_name=verif_user.first_name, last_name=verif_user.last_name, user_name=verif_user.user_name, user_pass=verif_user.user_pass)
        new_user.addToUsers()
        if type == "client":
            thiscompany = Company.query.filter_by(name=company).first()
            if thiscompany != None:
                new_client = Client(f_name=new_user.first_name, l_name=new_user.last_name, company=thiscompany)
                if new_client.addToClient():
                    new_client_ac = CLientAccount(client=new_client, user=new_user)
                    if new_client_ac.addToClientAccount():
                        verif_user.delToVerify()
        
        elif type == "employee":
            thiscompany = Company.query.filter_by(name=company).first()
            if thiscompany != None:
                new_employee = Employee(company=thiscompany, user=verif_user)
                if new_employee.addToEmployee():
                    verif_user.delToVerify()
