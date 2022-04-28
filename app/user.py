from datetime import date, timedelta
from flask import Blueprint, redirect,render_template, request, url_for
from database import mydatabase
 
user = Blueprint('user',__name__,url_prefix='/user')
dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='mydb.sqlite')


# @user.route('/home/',defaults ={"name":""})
@user.route('/home/<name>')
def user_home(name):
    res = dbms.print_all_data_books(table=mydatabase.BOOKS)
    custid = dbms.print_id_data_customers(name,table= mydatabase.CUSTOMERS)
    return render_template("urhome.html",name=name,res=res,custid=custid[0])

@user.route("/cust",methods=["POST","GET"])
def add_cust():
    name = request.form.get('name')
    city = request.form.get('city')
    age = request.form.get('age')
    dbms.insert_customers(name,city,age)
    return redirect(f"home/{name}")
    
@user.route('/about/',defaults ={"name":""})
@user.route("/about/<name>")
def ur_about(name):
    custid = dbms.print_id_data_customers(name,table= mydatabase.CUSTOMERS)
    return render_template("urabout.html",name=name,custid=custid[0])


@user.route("/addloan/<name>")
def add_loan(name):
    custid = request.args.get('custid')
    bookid = request.args.get('bookid')
    today = date.today()
    res =  dbms.check_type(bookid)
    if res[0] == 1:
        tenDays = date.today() + timedelta(days=10)
        dbms.insert_loans(custid,bookid,today,tenDays)
        print(custid,bookid,today,tenDays)
    if res [0]== 2:
        fiveDays = date.today() + timedelta(days=5)
        dbms.insert_loans(custid,bookid,today,fiveDays)
        print(custid,bookid,today,fiveDays)
    if res[0] == 3:
        twoDays = date.today() + timedelta(days=2)
        dbms.insert_loans(custid,bookid,today,twoDays)
        print(custid,bookid,today,twoDays)
    return user_home(name)

@user.route('/retbook/',defaults ={"name":""})   
@user.route('/retbook/<name>')
def user_loans(name):
    custid = dbms.print_id_data_customers(name,table= mydatabase.CUSTOMERS)
    res6 = dbms.print_data_loans(custid[0],table= mydatabase.LOANS)
    print(res6)
    return render_template("retbook.html",res6 = res6,name=name,custid=custid[0])

@user.route("/retloan")
def retLoan():
    custid = request.args.get('custid')
    bookid = request.args.get('bookid')
    custname = request.args.get('custname')
    dbms.delete_by_id_loans(custid,bookid)
    return user_loans(custname)