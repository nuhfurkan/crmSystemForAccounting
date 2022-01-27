from hashlib import new
from flask import Flask, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql
import sqlalchemy
from auth import User, verificationComplete
from config_db import Company, ToVerify, app

app.secret_key = "somekey"

# index page
@app.route("/")
def index():
    return render_template("index.html")

# client page # ENTRANCE PAGE # TO DO
@app.route("/client")
def client():
    return render_template("client.html")

# employee page # ENTRANCE PAGE # TO DO
@app.route("/employee") 
def employee():
    return render_template("employee.html")

# register section # TO DO
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST", "GET"])
def register_submit():
    name = request.form["name"]
    surname = request.form["surname"]
    user_name = request.form["user_name"]
    user_pass = request.form["user_pass"]
    pass_again = request.form["user_pass_again"]
    email = request.form["email"]
    companies = Company.query.all()
    if user_pass != pass_again:
        return render_template("register.html", invalid="no matching passwords")
    newToVerify = ToVerify(name, surname, user_name, user_pass, email)
    if newToVerify.addToVerify():
        return render_template("index.html", name=name)
    else:
        return render_template("register.html", invalid="something went wrong")

# employee sign in section
@app.route("/employeeEnter")
def employeeEnterPage():
    return render_template("employeeEnter.html")

@app.route("/employeeEnter", methods=["POST", "GET"])
def employeeEnter():
    username = request.form["name"]
    userpass = request.form["password"]
    newUser = User(username, userpass)
    if newUser.auth_employee() != False:
        session["type"] = "employee"
        session["id"] = newUser.id
        return render_template("index.html", name=newUser.id, idexists=newUser.id, ses_type=session["type"])
    return render_template('sign.html', invalid="incorrect entry")

# client sign in section
@app.route("/clientEnter")
def clientEnterPage():
    return render_template("clientEnter.html")

@app.route("/clientEnter", methods=["POST", "GET"])
def clientEnter():
    username = request.form["name"]
    userpass = request.form["password"]
    newUser = User(username, userpass)
    if newUser.auth_client() != False:
        session["type"] = "client"
        session["id"] = newUser.id
        return render_template("index.html", name=newUser.id, idexists=newUser.id, ses_type=session["type"])
    return render_template('sign.html', invalid="incorrect entry")

# verify
@app.route("/verify")
def verifyPage():
    all_companies = Company.query.all()
    return render_template("verify.html", company_data=all_companies)

@app.route("/verify", methods=["POST", "GET"])
def verify():
    all_companies = Company.query.all()
    user_email = request.form["user_email"]
    verification_code = request.form["verif_code"]
    type = request.form.get('type')
    company = request.form.get("companies")
    if verificationComplete(user_email, verification_code, type, company):
        return render_template("messagePage.html", my_message="succesfully verified")
    else:
        return render_template("verify.html", company_data=all_companies)

# message page
@app.route("/messagePage")
def messagePage():
    return render_template("messagePage.html")

# admin sign in section
# admin add new currency
# admin add new company
# employee add new vendor
# employee ad new BankAccount
# client add invoice
# employee response invoice
# employee create bill

# run the app
if __name__ == "__main__":
    app.run(port=5000, debug = True)