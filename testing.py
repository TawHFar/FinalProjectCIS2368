import flask
import cred
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