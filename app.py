from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql
import sqlalchemy
from auth import User
from config_db import ToVerify, app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/client")
def client():
    return render_template("client.html")

@app.route("/employee")
def employee():
    return render_template("employee.html")

#register section
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
    if user_pass != pass_again:
        return render_template("register.html", invalid="no matching passwords")
    newToVerify = ToVerify(name, surname, user_name, user_pass, email)
    if newToVerify.addToVerify():
        return render_template("index.html")
    else:
        return render_template("register.html", invalid="something went wrong")


#sign section
@app.route("/sign")
def sign():
    return render_template("sign.html")

@app.route('/sign',methods=['POST', 'GET'])
def sign_submit():
    username = request.form["name"]
    userpass = request.form["password"]
    newUser = User(username, userpass)
    if newUser.auth_user():
        return render_template("index.html")
    return render_template('sign.html', invalid="incorrect entry")

if __name__ == "__main__":
    app.run(port=5000, debug = True)