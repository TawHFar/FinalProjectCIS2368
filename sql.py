import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error {e} ocurred.")
    return connection

def execute_query(connection,query, values= None): #Chatgpt used to add parameter
    cursor = connection.cursor()
    try: 
        if values:
            cursor.execute(query,values)
        else:
            cursor.execute(query,values)
        connection.commit()
        print("Query executed succesfully")
    except Error as e:
        print(f'The error {e} occured.')


def execute_read_query(connection,query, values= None):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
         #Added parameters to read more parameters
         if values:
            cursor.execute(query,values)
            result = cursor.fetchall()
            return result
         else:
            cursor.execute(query,values)
            result = cursor.fetchall()
            return list(result)      
    except Error as e:
        print(f'The error {e} occured.')
