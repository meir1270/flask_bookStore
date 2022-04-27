from datetime import date, timedelta
from flask import Flask, redirect, render_template, request, url_for
from database import mydatabase
from app.admin import admin
from app.user import user

app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(user)

dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='mydb.sqlite')
# Program entry point
# Create Tables
dbms.create_db_tables()

@app.route("/",methods=["POST","GET"])
def home_view():
    if request.method == "POST":
        searchName = request.form.get('searchName')
        findBook = dbms.find_book_cust(searchName,table=mydatabase.BOOKS)
        return render_template('home.html',findBook=findBook)
    if request.method == "GET":
        res = dbms.print_all_data_books(table=mydatabase.BOOKS)
        return render_template('home.html',res=res)

@app.route("/login")
def login():
		return render_template("login.html")

@app.route("/about")
def about():
		return render_template("about.html")
