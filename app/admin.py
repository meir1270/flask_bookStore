from flask import Blueprint, redirect,render_template, request, url_for
from database import mydatabase
 
admin = Blueprint('admin',__name__,url_prefix='/admin')
dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='mydb.sqlite')

@admin.route('/books/<username>',methods=["POST","GET"])
def admin_member_books(username="test"):
    if request.method == "POST":
        searchName = request.form.get('searchName')
        findBook = dbms.find_book_cust(searchName,table=mydatabase.BOOKS)
        return render_template('adbooks.html',findBook=findBook,username=username)
    if request.method == "GET":
        res = dbms.print_all_data_books(table=mydatabase.BOOKS)
        return render_template("adbooks.html",username=username,res=res)
 
@admin.route('/customers/<username>',methods=["POST","GET"])
def admin_member_cust(username="test"): 
    if request.method == "POST":
        searchName = request.form.get('searchName')
        findBook = dbms.find_book_cust(searchName,table=mydatabase.CUSTOMERS)
        return render_template('adCust.html',findBook=findBook,username=username)
    if request.method == "GET":
        res =dbms.print_all_data_customers(table= mydatabase.CUSTOMERS)
        return render_template("adCust.html",username=username,res= res)

@admin.route('/loans/<username>')
def admin_member_loans(username=""):
    res = dbms.print_all_data_loans(table= mydatabase.LOANS)
    return render_template("adloans.html",username=username,res=res)

users = ["test",1234]
@admin.route("/auth",methods=["POST"])
def auth():
    error = "One of the details is incorrect"
    username = request.form.get('username')
    password = request.form.get('password')
    if username  in users:
        return redirect(f"books/{username}")
    else:
        return render_template("login.html",error=error)

@admin.route("/delbook")
def deleteBook():
    id = request.args.get('id')
    dbms.delete_by_id_books(id)
    return admin_member_books()


@admin.route("/delcust")
def deleteCust():
    id = request.args.get('id')
    dbms.delete_by_id_customers(id)
    return admin_member_cust()
    
@admin.route("/delloan")
def deleteLoan():
    custid = request.args.get('custid')
    bookid = request.args.get('bookid')
    dbms.delete_by_id_loans(custid,bookid)
    return admin_member_loans()
    

@admin.route("/addbook",methods=["POST"])
def admin_add_book():
    name = request.form.get('name')
    author = request.form.get('author')
    yearPublished = request.form.get('yearPublished')
    type = request.form.get('type')
    dbms.insert_books(name,author,yearPublished,type)
    return redirect("books/test")

@admin.route("/addcust",methods=["POST"])
def admin_add_cust():
    name = request.form.get('name')
    city = request.form.get('city')
    age = request.form.get('age')
    print(name,city,age)
    dbms.insert_customers(name,city,age)
    return redirect("customers/test")

@admin.route("/updatebook",methods=["POST"])
def admin_update_book():
    id = request.args.get('id')
    name = request.form.get('name')
    author = request.form.get('author')
    yearPublished = request.form.get('yearPublished')
    type = request.form.get('type')
    print(id,name,author,yearPublished,type)
    dbms.update_books(id,name,author,yearPublished,type)
    return redirect("books/test")
