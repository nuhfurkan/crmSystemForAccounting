from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import MetaData, Table, Column, Integer, String
import pymysql
import sqlalchemy
from app import db
import random
import string

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

db.create_all()