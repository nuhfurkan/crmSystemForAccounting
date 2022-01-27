from audioop import add
import email
from hashlib import new
from locale import currency
from flask import Flask, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql
import sqlalchemy
from auth import User, verificationComplete
from config_db import BankAccount, Company, Currency, Employee, ToVerify, Vendor, VendorDetails, app

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
        return render_template("messagePage.html", my_message="waiting for verification")
    else:
        return render_template("register.html", invalid="something went wrong")

# employee sign in section
@app.route("/employeeEnter")
def employeeEnterPage():
    return render_template("employeeEnter.html", ses_type=session["type"])

@app.route("/employeeEnter", methods=["POST", "GET"])
def employeeEnter():
    username = request.form["name"]
    userpass = request.form["password"]
    newUser = User(username, userpass)
    if newUser.auth_employee() == True:
        session["type"] = "employee"
        session["user"] = newUser.id
        session["company"] = Employee.query.filter_by(user=newUser.id).first().company
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
        session["user"] = newUser.id
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

# employee add new vendor
@app.route("/createNewVendor")
def createNewVendorPage():
    return render_template("createNewVendor.html", ses_type=session["type"])

@app.route("/createNewVendor", methods=["POST", "Get"])
def createNewVendor():
    vendor_name = request.form["vendor_name"]
    
    vendor_address = request.form["vendor_address"]
    vendor_zip = request.form["vendor_zip"]
    vendor_city = request.form["vendor_city"]
    vendor_country = request.form["vendor_country"]
    vendor_email = request.form["vendor_email"]
    vendor_phone = request.form["vendor_phone"]
    vendor_vat = request.form["vendor_vat"]
    vendor_commerce = request.form["vendor_commerce"]

    thecompany = Company.query.filter_by(id=session["company"]).first()
    new_vendor = Vendor(name=vendor_name, company=thecompany)
    if new_vendor.newVendor():
        new_vendor_det = VendorDetails(vendor=new_vendor, address=vendor_address, zip=vendor_zip, city=vendor_city, country=vendor_country, email=vendor_email, phone=vendor_phone, vat=vendor_vat, commerce=vendor_commerce)
        if new_vendor_det.newVendorDetails():
            return render_template("messagePage.html", my_message="created new vendor", ses_type=session["type"])
    return render_template("createNewVendor.html", message="something went wrong", ses_type=session["type"])

# employee add new BankAccount
@app.route("/newBankAccount")
def newBankAccountPage():
    currencies = Currency.query.all()
    return render_template("newBankAccount.html", ses_type=session["type"], currency_data=currencies)

@app.route("/newBankAccount", methods=["POST", "GET"])
def newBankAccount():
    currencies = Currency.query.all()
    init_amount = request.form["init_amount"]
    name = request.form["account_name"]
    iban = request.form["account_iban"]
    currency = request.form.get("currency")
    selected_currency = Currency.query.filter_by(name=currency).first()
    thecompany = Company.query.filter_by(id=session["company"]).first()
    new_account = BankAccount(start_amount=init_amount, name=name, iban=iban, curreny=selected_currency, company=thecompany)
    if new_account.createAccount():
        return render_template("messagePage.html", my_message="new account created succesfully", ses_type=session["type"])
    return render_template("newBankAccount.html", message="something went wrong", ses_type=session["type"], currency_data=currencies)

# admin sign in section
# admin add new currency
# admin add new company

# client add invoice

# employee response invoice
# employee create bill

# message page
@app.route("/messagePage")
def messagePage():
    return render_template("/messagePage.html")

# run the app
if __name__ == "__main__":
    app.run(port=5000, debug = True)