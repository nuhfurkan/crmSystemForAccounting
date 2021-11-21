import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import MetaData, Table, Column, Integer, String
import pymysql
import sqlalchemy
from sqlalchemy.orm import column_property
from werkzeug.datastructures import ContentSecurityPolicy
from app import client, db
import random
import string
import uuid
import datetime

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

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    user_name = db.Column(db.String(60))
    user_pass = db.Column(db.String(60))

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
        user.Client = client.id

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

class Company(db.Model):
    __tablename__ = "Company"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), nullable = False)
    default_currency = db.Column(db.Integer, db.ForeignKey("Currency.id"), nullable = False)

    def __init__(self, name, curreny):
        self.name = name
        self.default_currency = curreny

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

    def __init__(self, clint, address, zip, city, country, email, phone, vat, commerce):
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

    def __init__(self, client, currency, referance):
        self.client = client.id
        self.currency = currency.id
        self.referance = referance.id

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

db.create_all()