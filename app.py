from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql
import sqlalchemy

app = Flask(__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/crmDatabase?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/client")
def client():
    return render_template("client.html")

@app.route("/employee")
def employee():
    return render_template("employee.html")

if __name__ == "__main__":
    app.run(port=5000, debug = True)