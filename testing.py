import flask
import cred
from datetime import datetime
from sql import create_connection
from sql import execute_read_query
from sql import execute_query #added this import to have access add and delete to query
from flask import jsonify
from flask import request


app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

#Connect to database
myCreds = cred.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)


# Using class notes, use GET functipn to retrieve all barbells
@app.route('/api/books', methods=['GET'])
def get_books():
    query = "SELECT * FROM books"
    book = execute_read_query(conn, query)
    return jsonify(list(book))


#Using the class notes for the request data and used Chatgpt suggestion to
#make an values to add the query 
@app.route('/api/books', methods=['POST'])
def add_book():

    #Used the class note format to request the information
    request_data = request.get_json()
    title = request_data['title']
    author = request_data['author']
    genre = request_data['genre']
    status = request_data['status']

    query = """
        INSERT INTO books (title, author, genre, status) 
        VALUES (%s,%s,%s,%s)"""
    
    values = (title, author, genre, status)
    
    execute_query(conn, query, values)

    return "Book added successfully"


#crud function to updating a book
@app.route('/api/books/<int:id>', methods = ['PUT'])
def update_book(id):
    request_data = request.get_json() #used chatgpt to use .get to return none of title is not provided 
    update_title = request_data.get('title')
    update_author = request_data.get('author')
    update_genre = request_data.get('genre')
    update_status = request_data.get('status')

    #used chatgpt to figure out how to update different parts of the record
    query = "UPDATE books SET"
    values = []

    #used chatgpt to figure out errors in postman and lost set clause parts 
    set_clauses = []

    if update_title: 
        set_clauses.append("title = %s")
        values.append(update_title)
    if update_author: 
        set_clauses.append("author = %s")
        values.append(update_author)
    if update_genre: 
        set_clauses.append("genre = %s")
        values.append(update_genre)
    if update_status: 
        set_clauses.append("status = %s")
        values.append(update_status)
    #used chatgpt to fix spacing error 
    query +=" "+", ".join(set_clauses) + " WHERE id = %s" #https://www.w3schools.com/python/ref_string_join.asp
    values.append(id)

    execute_query(conn, query, tuple(values))

    return "Book Updated"

@app.route('/api/books/delete', methods=['DELETE'])
def delete_book():
    request_data = request.get_json()
    book_id = request_data['id']
    query_check = "SELECT * FROM WHERE id = %s" #checks if book exist
    result = execute_read_query(conn, query_check, (book_id,))
#used chatgpt for error cheching 
    if not result:
        "Book not in inventory"


    query = "DELETE FROM books WHERE id = %s"
    values = (book_id,)

    execute_query(conn, query, values)
    return "Books deleted succesfully"


# Using class notes, use GET functipn to retrieve all customers
@app.route('/api/customers', methods=['GET'])
def get_customer():
    query = "SELECT * FROM customers"
    customer = execute_read_query(conn, query)
    return jsonify(list(customer))


@app.route('/api/customers', methods=['POST'])
def add_customer():

    #Used the class note format to request the information
    request_data = request.get_json()
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    email = request_data['email']
    pwhash = request_data['passwordhash']

    new_entry = """
        INSERT INTO customers (firstname, lastname, email, passwordhash) 
        VALUES (%s, %s, %s, %s)"""
    
    values = (firstname, lastname, email, pwhash)
    
    execute_query(conn, new_entry, values)

    return "Profile added successfully"

@app.route('/api/customers/<int:id>', methods = ['PUT'])
def update_customer(id):
    request_data = request.get_json() #used chatgpt to use .get to return none of title is not provided 
    update_firstname = request_data.get('firstname')
    update_lastname = request_data.get('lastname')
    update_email = request_data.get('email')
    update_pwhash = request_data.get('passwordhash')

    #used chatgpt to figure out how to update different parts of the record
    query = "UPDATE books SET"
    values = []

    #used chatgpt to figure out errors in postman and lost set clause parts 
    set_clauses = []

    if update_firstname: 
        set_clauses.append("firstname = %s")
        values.append(update_firstname)
    if update_lastname: 
        set_clauses.append("lastname = %s")
        values.append(update_lastname)
    if update_email: 
        set_clauses.append("email = %s")
        values.append(update_email)
    if update_pwhash: 
        set_clauses.append("passwordhash = %s")
        values.append(update_pwhash)
    #used chatgpt to fix spacing error 
    query +=" "+", ".join(set_clauses) + " WHERE id = %s" #https://www.w3schools.com/python/ref_string_join.asp
    values.append(id)

    execute_query(conn, query, tuple(values))

    return "Book Updated"


@app.route('/api/customers/delete', methods=['DELETE'])
def delete_customers():
    request_data = request.get_json()
    cust_id = request_data['id']
    query_check = "SELECT * FROM WHERE id = %s" #checks if customer exist
    result = execute_read_query(conn, query_check, (cust_id,))
#used chatgpt for error cheching 
    if not result:
        "Profile not found"


    query = "DELETE FROM customers WHERE id = %s"
    values = (cust_id,)

    execute_query(conn, query, values)
    return "Profile deleted succesfully"



#Using table borrowrecords to allow user to check out a book
@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    request_data = request.get_json()
    book_id = request_data['bookid']
    cust_id = request_data['customerid']
    borrow_date = request_data['borrowdate']
    format_date = datetime.strptime(borrow_date, '%Y-%m-%d')

    #Checks status book if available to check out
    book_query = 'SELECT status FROM books WHERE id=%s'
    book_value = (book_id,)
    check_query = execute_read_query(conn, book_query, book_value)
#used chatgpt tp fix check query error
    if not check_query  or check_query[0]['status'] != 'Available':
        return "Book unavailable."
    
    #Checks if customer is in borrowing records and confirms if they are able to borrow book
    borrow_query = 'SELECT * FROM borrowingrecords WHERE customerid=%s AND returndate IS NULL'
    cust_value = (cust_id,)
    check_cust = execute_read_query(conn, borrow_query, cust_value)

    if check_cust:
        return "Customer has already borrowed a book."
    
    #Inserted information of the checkout 
    new_borrowquery = """INSERT INTO borrowingrecords (bookid,customerid,borrowdate) VALUES (%s,%s,%s)"""
    new_values = (book_id,cust_id,format_date)
    execute_query(conn, new_borrowquery, new_values)

    #Upated book status
    update_status = "UPDATE books SET status ='Unavailable' WHERE id=%s"
    execute_query(conn,update_status,(book_id,))

    return "Book Borrowed Successfully!"

@app.route('/api/return_date/<int:id>', methods =['PUT'])
def return_book(id):
    request_data = request.get_json()
    borrow_id = request_data['id']
    return_date_str = request_data['returndate']

    return_date = datetime.strptime(return_date_str, '%Y-%m-%d') #https://www.geeksforgeeks.org/python-datetime-strptime-function/

    select_query = "SELECT borrowdate,bookid FROM borrowingrecords WHERE id = %s"
    borrow_result = execute_read_query(conn, select_query,(id,))

    if not borrow_result:
        return "Borrow record not found"
    
    borrow_date_str = borrow_result[0]['borrowdate']
    book_id = borrow_result[0]['bookid']

    if isinstance(borrow_date_str, str):#https://www.w3schools.com/python/ref_func_isinstance.asp
        borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d')
    else:
        borrow_date = borrow_date_str
#calculate the difference in days 
    return_date = return_date.date() #used chatgpt to fix this error 

    day_difference = (return_date - borrow_date).days
    late_fee = 0
    if day_difference > 10: 
        late_fee = day_difference - 10

    update_query  =""" 
    UPDATE borrowingrecords 
    SET returndate = %s, late_fee = %s
    WHERE id  = %s
    """
    execute_query(conn, update_query,(return_date_str,late_fee,id))

    #update book status 
    update_book_status = "UPDATE books SET status = 'Unavailable' WHERE id = %s"
    execute_query(conn, update_book_status,(book_id,))

    return jsonify ({"Return Date updated"})

# Using class notes, use GET function to retrieve borrowingrecord 
@app.route('/api/borrowingrecords', methods=['GET'])
def get_records():
    query = "SELECT * FROM borrowingrecords"
    records = execute_read_query(conn, query)
    return jsonify(records)

app.run()