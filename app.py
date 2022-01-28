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
from config_db import Admin, BankAccount, Company, Currency, Employee, ToVerify, Vendor, VendorDetails, app


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
        return render_template("employee.html", ses_type=session["type"])
    return render_template('employeeEnter.html', invalid="incorrect entry")

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
@app.route("/admin")
def adminPage():
    return render_template("admin.html")

@app.route("/admin", methods=["POST", "GET"])
def admin():
    admin_name = request.form["admin_name"]
    admin_pass = request.form["admin_pass"]
    admin = Admin.query.filter_by(admin_name=admin_name,admin_pass=admin_pass).first()
    if admin != None:
        session["type"] = "admin"
        #session["user"] = admin.id
        return render_template("adminPanel.html")
    return render_template("admin.html", message="invalid name or pass")

# admin add new currency
@app.route("/currencies", methods=["POST", "GET"])
def currenciesPage():
    currencies = Currency.query.all()
    data = []
    for currency in currencies:
        newdata = {}
        newdata["id"] = currency.id
        newdata["name"] = currency.name
        newdata["code"] = currency.code
        data.append(newdata)

    return render_template("currencies.html", rowdata=data, ses_type=session["type"])

@app.route("/deleteRow")
def deleteRow():
    mid = request.args.get("mid")
    toDel = Currency.query.filter_by(id=mid).first()
    if toDel != None:
        toDel.delCurrency()
        return currenciesPage()
    return render_template("currencies.html", message="something went wrong")

@app.route("/addToCurrencies", methods=["POST", "GET"])
def addToCurrencies():
    print("created new currency")
    cr_name = request.form["currency_name"]
    cr_code = request.form["currency_code"]
    newCr = Currency(name=cr_name, code=cr_code)
    if newCr.createCurrency():
        return currenciesPage()
    return render_template("currencies.html", message="something went wrong")

# admin add new company
@app.route("/companies", methods=["POST", "GET"])
def companiesPage():
    companies = Company.query.all()
    currencies = Currency.query.all()
    data = []
    for company in companies:
        newdata = {}
        newdata["id"] = company.id
        newdata["name"] = company.name
        newdata["default_currency"] = company.default_currency
        data.append(newdata)
    
    return render_template("companies.html", rowdata=data, currency_data=currencies)

@app.route("/deleteCompany")
def deleteCompany():
    mid = request.args.get("mid")
    toDel = Company.query.filter_by(id=mid).first()
    if toDel != None:
        if toDel.delCompany():
            return companiesPage()
    return render_template("companies.html", message="something went wrong")

@app.route("/addToCompanies", methods=["POST", "GET"])
def addToCompanies():
    companyname = request.form["company_name"]
    def_currency = request.form["default_currency"]
    mycurreny = Currency.query.filter_by(name=def_currency).first()
    if mycurreny != None:
        newComp = Company(name=companyname, curreny=mycurreny.id)
        if newComp.addCompany():
            return companiesPage()
    return render_template("companies.html", message="something went wrong")

# client add invoice


# employee response invoice
# employee create bill

# message page
@app.route("/messagePage")
def messagePage():
    return render_template("messagePage.html")

# run the app
if __name__ == "__main__":
    app.run(port=5000, debug = True)