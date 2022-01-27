from distutils.command.build_scripts import first_line_re
from os import name
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import MetaData, Table, Column, Integer, String
import pymysql
import sqlalchemy
from sqlalchemy.orm import column_property
from werkzeug.datastructures import ContentSecurityPolicy, ImmutableHeadersMixin
import random
import string
import uuid
import datetime

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/crmDatabase?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToVerify(db.Model):
    __tablename__ = "ToVerify"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    user_name = db.Column(db.String(60))
    user_pass = db.Column(db.String(60))
    email = db.Column(db.String(60))
    verification_code = db.Column(db.String(20))

    def __init__(self, firs_name, last_name, user_name, user_pass, email):
        self.first_name = firs_name
        self.last_name = last_name
        self.user_name = user_name
        self.user_pass = user_pass
        self.email = email
        self.verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))

    def addToVerify(self):
        db.session.add(self)
        db.session.commit()   
        print("new user added toveirfy")
        return True

    def delToVerify(self):
        db.session.delete(self)
        db.session.commit()
        print("deleted toVeriy with name " + self.first_name + " " + self.last_name + " with id " + str(self.id))
        return True

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    user_name = db.Column(db.String(60))
    user_pass = db.Column(db.String(60))

    def addToUsers(self):
        db.session.add(self)
        db.session.commit()
        print("new user added to users")
        return True

    def __init__(self, firs_name, last_name, user_name, user_pass):
        self.first_name = firs_name
        self.last_name = last_name
        self.user_name = user_name
        self.user_pass = user_pass

class CLientAccount(db.Model):
    __tablename__ = "ClientAccount"
    id = db.Column(db.Integer, primary_key = True)
    Client = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable = False)
    User = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = False)

    def __init__(self, user, client):
        self.User = user.id
        self.Client = client.id

    def addToClientAccount(self):
        db.session.add(self)
        db.session.commit()
        print("new ClinetAccount added")
        return True

class Client(db.Model):
    __tablename__ = "Client"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    company = db.Column(db.Integer, db.ForeignKey("Company.id"), nullable = False)
    uuid = db.Column(db.String(120))

    def __init__(self, f_name, l_name, company):
        self.first_name = f_name
        self.last_name = l_name
        self.company = company.id 
        self.uuid = uuid.uuid1

    def addToClient(self):
        db.session.add(self)
        db.session.commit()
        print("new client added")
        return True

class Company(db.Model):
    __tablename__ = "Company"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), nullable = False)
    default_currency = db.Column(db.Integer, db.ForeignKey("Currency.id"), nullable = False)

    def __init__(self, name, curreny):
        self.name = name
        self.default_currency = curreny

class CompanyDetails(db.Model):
    __tablename__ = "CompanyDetails"
    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.Integer, db.ForeignKey("Company.id"), nullable = False)
    address = db.Column(db.String(160), nullable = False)
    zip = db.Column(db.String(20), nullable = False)
    city = db.Column(db.String(60), nullable = False)
    country = db.Column(db.String(60), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    vat_id = db.Column(db.String(60), nullable = False)
    commerce_id = db.Column(db.String(60), nullable = False)

    def __init__(self, company, address, zip, city, country, email, phone, vat_id, commerce_id):
        self.companc = company.id
        self.address = address
        self.zip = zip
        self.city = city
        self.country = country
        self.email = email
        self.phone = phone
        self.vat_id = vat_id
        self.commerce_id = commerce_id

class Currency(db.Model):
    __tablename__ = "Currency"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    code = db.Column(db.String(5), nullable = False)

    def __init__(self, name, code):
        self.name = name
        self.code = code

class ClientDetails(db.Model):
    __tablename__ = "ClientDetails"
    id = db.Column(db.Integer, primary_key = True)
    client = db.Column(db.Integer, db.ForeignKey("Client.id"), nullable = False)
    address = db.Column(db.String(160), nullable = False)
    zip = db.Column(db.String(20), nullable = False)
    city = db.Column(db.String(60), nullable = False)
    country = db.Column(db.String(60), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    vat = db.Column(db.String(60), nullable = False)
    commerce = db.Column(db.String(60), nullable = False)

    def __init__(self, client, address, zip, city, country, email, phone, vat, commerce):
        self.client = client.id
        self.address = address
        self.zip = zip
        self.city = city
        self.country = country
        self.email = email
        self.phone = phone
        self.vat = vat
        self.commerce = commerce

class Invoice(db.Model):
    __tablename__ = "Invoice"
    id = db.Column(db.Integer, primary_key = True)
    client = db.Column(db.Integer, db.ForeignKey("Client.id"), nullable = False)
    currency = db.Column(db.Integer, db.ForeignKey("Currency.id"), nullable = False)
    uuid = db.Column(db.String(120))
    referance = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = True)

    def __init__(self, client, currency):
        self.client = client.id
        self.currency = currency.id
        self.uuid = uuid.uuid1


    def __init__(self, client, currency, referance):
        self.client = client.id
        self.currency = currency.id
        self.referance = referance.id
        self.uuid = uuid.uuid1


class InvoiceSent(db.Model):
    __tablename__ = "InvoiceSent"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    invoice = db.Column(db.Integer, db.ForeignKey("Invoice.id"), nullable = False)

    def __init__(self, invoice):
        self.date = datetime.datetime.utcnow()
        self.invoice = invoice.id

class InvoiceViewed(db.Model):
    __tablename__ = "InvoiceViewed"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    invoice = db.Column(db.Integer, db.ForeignKey("Invoice.id"), nullable = False)

    def __init__(self, invoice):
        self.date = datetime.datetime.utcnow()
        self.invoice = invoice.id

class InvoicePaid(db.Model):
    __tablename__ = "InvoicePaid"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    invoice = db.Column(db.Integer, db.ForeignKey("Invoice.id"), nullable = False)

    def __init__(self, invoice):
        self.date = datetime.datetime.utcnow()
        self.invoice = invoice.id

class InvoiceItem(db.Model):
    __tablename__ = "InvoiceItem"
    id = db.Column(db.Integer, primary_key = True)
    invoice = db.Column(db.Integer, db.ForeignKey("Invoice.id"), nullable = False)
    price = db.Column(db.Float, nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    item = db.Column(db.Integer, db.ForeignKey("Item.id"), nullable = False)

    def __init__(self, price, amount, invoice, item):
        self.invoice = invoice.id
        self.price = price
        self.amount = amount
        self.item = item.id

class Item(db.Model):
    __tablename__ = "Item"
    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.Integer, db.ForeignKey("Company.id"))
    description = db.Column(db.String(240))
    default_price = db.Column(db.Float)
    uuid = db.Column(db.String(120))

    def __init__(self, company, description, default_price):
        self.company = company.id
        self.description = description
        self.default_price = default_price
        self.uuid = uuid.uuid1

class BillItem(db.Model):
    __tablename__ = "BillItem"
    id = db.Column(db.Integer, primary_key = True)
    bill = db.Column(db.Integer, db.ForeignKey("Bill.id"), nullable = False)
    item = db.Column(db.Integer, db.ForeignKey("Item.id"), nullable = False)
    price = db.Column(db.Float, nullable = False)
    amount = db.Column(db.Integer, nullable = False)

    def __init__(self, bill, item, price, amount):
        self.bill = bill.id
        self.item = item.id
        self.price = price
        self.amount = amount

class Bill(db.Model):
    __tablename__ = "Bill"
    id = db.Column(db.Integer, primary_key = True)
    vendor = db.Column(db.Integer, db.ForeignKey("Vendor.id"), nullable = False)
    currency = db.Column(db.Integer, db.ForeignKey("Currency.id"), nullable = False)
    date = db.Column(db.DateTime)
    uuid = db.Column(db.String(120))
    referance = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = True)

    def __init__(self, vendor, currency, referance):
        self.vendor = vendor.id
        self.currency = currency.id
        self.referance = referance
        self.uuid = uuid.uuid1
        self.date = datetime.datetime.utcnow()

class Vendor(db.Model):
    __tablename__ = "Vendor"
    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.Integer, db.ForeignKey("Company.id"))
    name = db.Column(db.String(30))
    uuid = db.Column(db.String(120))

    def __init__(self, name, company):
        self.name = name
        self.company = company.id
        self.uuid = uuid.uuid1()

    def newVendor(self):
        db.session.add(self)
        db.session.commit()
        print("new vendor created")
        return True

class VendorDetails(db.Model):
    __tablename__ = "VendorDetails"
    id = db.Column(db.Integer, primary_key = True)
    vendor = db.Column(db.Integer, db.ForeignKey("Vendor.id"), nullable = False)
    address = db.Column(db.String(160), nullable = False)
    zip = db.Column(db.String(20), nullable = False)
    city = db.Column(db.String(60), nullable = False)
    country = db.Column(db.String(60), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    vat = db.Column(db.String(60), nullable = False)
    commerce = db.Column(db.String(60), nullable = False)

    def __init__(self, vendor, address, zip, city, country, email, phone, vat, commerce):
        self.vendor = vendor.id
        self.address = address
        self.zip = zip
        self.city = city
        self.country = country
        self.email = email
        self.phone = phone
        self.vat = vat
        self.commerce = commerce

    def newVendorDetails(self):
        db.session.add(self)
        db.session.commit()
        print("new vendor details added")
        return True

class Employee(db.Model):
    __tablename__ = "Employee"
    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.Integer, db.ForeignKey("Company.id"), nullable = False)
    user = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = False)

    def __init__(self, company, user):
        self.company = company.id
        self.user = user.id

    def addToEmployee(self):
        db.session.add(self)
        db.session.commit()
        print("new employee added")
        return True

class BankAccount(db.Model):
    __tablename__ = "BankAccount"
    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.Integer, db.ForeignKey("Company.id"), nullable = False)
    start_amount = db.Column(db.Float, nullable = False)
    name = db.Column(db.String(30))
    iban = db.Column(db.String(120))
    uuid = db.Column(db.String(120))
    currency = db.Column(db.Integer, db.ForeignKey("Currency.id"), nullable = False)

    def __init__(self, start_amount, name, iban, curreny, company):
        self.company = company.id
        self.start_amount = start_amount
        self.name = name
        self.iban = iban
        self.currency = curreny.id
        self.uuid = uuid.uuid1()

    def createAccount(self):
        db.session.add(self)
        db.session.commit()
        print("new account created")
        return True

def config_init():
    db.create_all()