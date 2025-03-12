import flask
import cred
import datetime
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
    return jsonify(book)


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

    new_entry = """
        INSERT INTO inventory (title, author, genre, status) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
    
    values = (title, author, genre, status)
    
    execute_query(conn, new_entry, values)

    return "Book added successfully"

#crud function to updating a book
@app.route('/api/book/<int:id>', methods = ['PUT'])
def update_book():
    request_data = request.get_json()
    book_id = request_data['id']
    update_title = request_data['title']
    update_author = request_data['author']
    update_genre = request_data['genre']
    update_status = request_data['status']

    #used chatgpt to figure out how to update different parts of the record
    query = "UPDATE books SET"
    values = []

    if update_title: 
        query += "title = %s"
        values.append(update_title)
    if update_author: 
        query += "author = %s"
        values.append(update_author)
    if update_genre: 
        query += "genre = %s"
        values.append(update_genre)
    if update_status: 
        query += "status = %s"
        values.append(update_status)
    
    query += "WHERE id = %s"
    values.append(book_id)

    execute_query(conn, query, tuple(values))

    return "Book Updated"

@app.route('/api/books/delete', methods=['DELETE'])
def delete_book():
    request_data = request.get_json()
    customer_id = request_data['id']
    result = execute_read_query(conn, query, customer_id)

    if not result:
        "Customer not in inventory"


    query = "SELECT  FROM books WHERE id = %s"
    values = (customer_id,)

    execute_query(conn, query, values)
    return "Books deleted succesfully"





# Using class notes, use GET functipn to retrieve all barbells
@app.route('/api/customers', methods=['GET'])
def get_customer():
    query = "SELECT * FROM customer"
    customer = execute_read_query(conn, query)
    return jsonify(customer)


@app.route('/api/customer', methods=['POST'])
def add_customer():

    #Used the class note format to request the information
    request_data = request.get_json()
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    email = request_data['email']
    pwhash = request_data['passwordhash']


    new_entry = """
        INSERT INTO inventory (firstname, lastname, email, passwordhash) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
    
    values = (firstname, lastname, email, pwhash)
    
    execute_query(conn, new_entry, values)

    return "Profile added successfully"

@app.route('/api/customer/<int:id>', methods = ['PUT'])
def update_customer():
    request_data = request.get_json()
    cust_id = request_data['id']
    update_firstname = request_data['firstname']
    update_lastname = request_data['lastname']
    update_email = request_data['email']
    update_passwordhash = request_data['passwordhash']

    #used chatgpt to figure out how to update different parts of the record
    query = "UPDATE books SET"
    values = []

    if update_firstname: 
        query += "firstname = %s"
        values.append(update_firstname)
    if update_lastname: 
        query += "lastname = %s"
        values.append(update_lastname)
    if update_email: 
        query += "email = %s"
        values.append(update_email)
    if update_passwordhash: 
        query += "passwordhash = %s"
        values.append(update_passwordhash)
    
    query += "WHERE id = %s"
    values.append(cust_id)

    execute_query(conn, query, tuple(values))

    return "Customer Updated"


@app.route('/api/customer/delete', methods=['DELETE'])
def delete_customer(id):
    request_data = request.get_json()
    book_id = request_data['id']
    result = execute_read_query(conn, query, book_id)

    if not result:
        "Book not in inventory"


    query = "SELECT  FROM books WHERE id = %s"
    values = (id,)

    execute_query(conn, query, values)
    return "Customer deleted succesfully"



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

    if check_query != 'available':
        return "Book unavailable."
    
    #Checks if customer is in borrowing records and confirms if they are able to borrow book
    borrow_query = 'SELECT * FROM borrowingrecords WHERE customerid=%s AND returndate is NULL'
    cust_value = (cust_id)
    check_cust = execute_read_query(conn, borrow_query, cust_value)

    if check_cust:
        return "Customer has already borrowed a book."
    
    #Inserted information of the checkout 
    new_borrowquery = """INSERT INTO borrowrecords (bookid,custimerid,borrowdate) VALUES %s,%s,%s"""
    new_values = (book_id,cust_id,format_date)
    execute_query(conn, new_borrowquery, new_values)

    #Upated book status
    update_status = "UPDATE books SET status ='unavailable' WHERE id=%s"
    new_values = (book_id,)
    execute_query(conn,update_status,new_values)

    return "Book Borrowed Successfully!"

@app.route('/return_date', methods =['PUT'])
def return_book(id):
    request_data = request.get_json()
    borrow_id = request_data['id']
    return_date_str = request_data['returndate']

    return_date = datetime.strptime(return_date_str, '%Y-%m-%d')

    select_query = "SELECT borrowdate FROM borrowingrecords WHERE id = {id}"
    borrow_result = execute_read_query(conn, select_query)

    if not borrow_result:
        return jsonify({"Borrow record not found"})
    
    borrow_date_str = borrow_date[0]['borrowdate']
    borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d')
#calculate the difference in days 
    day_difference = (return_date - borrow_date).days

    late_fee = 0
    if day_difference > 10: 
        late_fee = day_difference - 10

    update_query  =f""" 
    UPDATE borrowingrecords 
    SET returndate = '{return_date_str}', latefee = {late_fee}
    WHERE id  = {id}
    """
    execute_query(conn, update_query)

    return jsonify ({"Return Date updated"})

app.run()