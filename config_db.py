from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql
import sqlalchemy
from app import db

app = Flask(__name__)

class Suggestion(db.Model):
    __tablename__ = 'second'
    id   = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))

    def __init__( self, name ):
        self.name = name

db.create_all()
print("done")