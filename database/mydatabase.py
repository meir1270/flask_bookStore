from sqlalchemy import  Date, UniqueConstraint, create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from datetime import date, datetime, timedelta
from sqlalchemy.orm import relationship

# Global Variables
SQLITE                  = 'sqlite'

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# Table Names
BOOKS           = 'books'
CUSTOMERS       = 'customers'
LOANS           ="loans"

class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///db.sqlite3',
    }
    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(engine_url)
            print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")

    def BookSelect(type):
        if type == "1":
                return datetime.now() + timedelta(days=10)
        elif type == "2":
            return datetime.now() + timedelta(days=5)
        elif type == "3":
            return datetime.now() + timedelta(days=2)


    def create_db_tables(self):
    
        metadata = MetaData()
        books = Table(BOOKS, metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String,nullable=False),
            Column('author', String),
            Column('yearPublished', String),
            Column('type', Integer,nullable=False)
                 )   
        customers = Table(CUSTOMERS, metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(20),unique=True,nullable=False),
            Column('city', String),
            Column('age', String),
                )
        loans = Table(LOANS, metadata,
                Column('custid', None, ForeignKey('customers.id')),
                Column('bookid', None, ForeignKey('books.id')),
                Column('loandate',Date),
                Column('returndate', Date)
                )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return
        else:
            print (query)
            with self.db_engine.connect() as connection:
                try:
                    connection.execute(query)
                except Exception as e:
                    print(e)

    def check_type(self,bookid,query=''):
        query = query if query != '' else f"SELECT type FROM BOOKS WHERE id = {bookid};"
        print(query)
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                    # print(row) # print(row[0], row[1], row[2])
                result.close()
        # print("\n")
        return res [0]   

    def print_all_data_books(self, table='', query=''):
        query = query if query != '' else f"SELECT * FROM '{table}';"
        print(query)
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                    # print(row) # print(row[0], row[1], row[2])
                result.close()
        # print("\n")
        return res

        
    def find_book_cust(self,name, table='', query=''):
        query = query if query != '' else f"SELECT * FROM '{table}' WHERE name LIKE '%{name}%';"
        print(query)
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                    # print(row) # print(row[0], row[1], row[2])
                result.close()
        # print("\n")
        return res

    
    def print_all_data_customers(self, table='', query=''):
        query = query if query != '' else f"SELECT * FROM '{table}';"
        print(query)
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                    # print(row) # print(row[0], row[1], row[2])
                result.close()
        # print("\n")
        return res

    def print_id_data_customers(self,name,table='',query=''):
        query = query if query != ''else f"SELECT id FROM '{table}' WHERE name ='{name}';"
        print(query)
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                 for row in result:
                    res.append( row)
                    # print(row) # print(row[0], row[1], row[2])
                 result.close()
         # print("\n")
        return res[0]

    def print_all_data_loans(self, table='', query=''):
        query = query if query != '' else f"SELECT * FROM {table};"
        print(query)
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                    # print(row) # print(row[0], row[1], row[2])
                result.close()
        # print("\n")
        return res

    def print_data_loans(self,custid, table='', query=''):
        query = query if query != '' else \
         f"SELECT LOANS.loandate,LOANS.returndate, Customers.name as custname, BOOKS.name, BOOKS.id as bookid, Customers.id as custid \
            FROM (({table}   \
            INNER JOIN Customers ON LOANS.custid = Customers.id) \
            INNER JOIN BOOKS ON LOANS.bookid = BOOKS.id) \
            where custid = {custid};"
        print(query)
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                # print(row) # print(row[0], row[1], row[2])
                result.close()
             # print("\n")
            return res


    # Examples

    # def sample_query(self):
    #     # Sample Query
    #     query = "SELECT name, author, yearPublished, type  FROM {TBL_USR} WHERE " \
    #             .format(TBL_USR=BOOKS)
    #     self.print_all_data(query=query)

    #     query = "SELECT name, city, age FROM {TBL_USR} WHERE " \
    #             .format(TBL_USR=CUSTOMERS)
    #     self.print_all_data(query=query)

    #     # Sample Query Joining
    #     query = "SELECT b.name as book_name, " \
    #             "c.name as cust_name " \
    #             "FROM {TBL_LOAN} AS l " \
    #             "LEFT JOIN {TBL_BOOKS} as b " \
    #             "LEFT JOIN {TBL_CUST} as c " \
    #             "WHERE b.id=l.bookid AND c.id=l.custid;" \
    #         .format(TBL_BOOKS=BOOKS, TBL_CUST=CUSTOMERS,TBL_LOAN= LOANS)
    #     self.print_all_data(query=query)

    def delete_by_id_books(self,id):
        # Delete Data by Id
        query = f"DELETE FROM BOOKS WHERE id={id}"
        self.execute_query(query)
        # self.print_all_data(table)

    def delete_by_id_customers(self,id):
        # Delete Data by Id
        query = f"DELETE FROM CUSTOMERS WHERE id={id}"
        self.execute_query(query)

    def delete_by_id_loans(self,custid,bookid):
        # Delete Data by Id
        query = f"DELETE FROM LOANS WHERE custid={custid} and bookid={bookid}"
        self.execute_query(query)

        # Delete All Data
        '''
        query = "DELETE FROM {}".format(USERS)
        self.execute_query(query)
        self.print_all_data(USERS)
        '''

            
    def insert_books(self,name ,author, yearPublished ,type):
            # Insert Data
        query = f"INSERT INTO BOOKS(name, author ,yearPublished , type ) " \
                f"VALUES ('{name}','{author}','{yearPublished}',{type});"
        # print(query)
        self.execute_query(query)
        # self.print_all_data(BOOKS)

    def insert_customers(self,name, city, age):
        # Insert Data to customers
        query = f"INSERT INTO CUSTOMERS( name, city, age) " \
                f"VALUES ('{name}','{city}', {age});"
        # print(query)
        self.execute_query(query)
        # self.print_all_data(CUSTOMERS)

    def insert_loans(self, custid,bookid,loandate,returndate):
        # Insert Data
        query = f"INSERT INTO LOANS( custid, bookid, loandate,returndate) " \
                f"VALUES ( {custid},{bookid},'{loandate}','{returndate}');"
        # print(query)
        self.execute_query(query)
        # self.print_all_data(LOANS) 


    def update_books(self,whatToUp,value,id):
        # Update books Data 
        query = f"UPDATE books set {whatToUp}='{value}' WHERE id={id}"
        self.execute_query(query)
        self.print_all_data(BOOKS)

    def update_customers(self,whatToUp,value,id):
        # Update customers Data
        query = f"UPDATE CUSTOMERS set {whatToUp}='{value}' WHERE id={id}"
        self.execute_query(query)
        # self.print_all_data(CUSTOMERS)

    def update_loans(self,whatToUp,value,id):
        # Update loans Data
        query = f"UPDATE LOANS set {whatToUp}='{value}' WHERE id={id}"
        self.execute_query(query)
        self.print_all_data(LOANS)