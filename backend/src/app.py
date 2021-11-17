from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_mysqldb import MySQL

from macros import Macros
from utils import Utils
from database import Database

import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = Macros.SECRETE_KEY

# DB connection details
# app.config['MYSQL_HOST'] = Macros.MYSQL_HOST
app.config['MYSQL_USER'] = Macros.MYSQL_USER
# app.config['MYSQL_PASSWORD'] = Macros.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Macros.MYSQL_DB #str(Macros.DB_FILE)

mysql = MySQL(app)
Macros.DB_DIR.mkdir(parents=True, exist_ok=True)

@app.route("/api/status", methods=['GET'])
def status():
  return "running"

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method =='POST' and \
       'username' in request.form and \
       'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #username = Utils.hashing(username)
        #password = Utils.hashing(password)
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        account = Database.user_exists_in_db(cursor, mysql, username, hash_password=password)
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = "Successfully logged in!"
        else:
            msg = 'Incorrect username/password!'
        # end if
    # end if
    
    cursor.close()
    print(msg)
    return jsonify(
        msg=msg
    )

# http://localhost:5000/api/logout
# This will be the logout page
@app.route('/api/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    
    msg = 'Successfully logged out'
    return jsonify(
        msg=msg
    )

# http://localhost:5000/api/register
# this will be the registration page, we need to use both GET and POST requests
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = 'No input parameters'
    #register_html = Macros.FRONTEND_DIR / 'register.html'
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and \
       'username' in request.form and\
       'password' in request.form and \
       'email' in request.form:
        
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hash_username = Utils.hashing(username)
        hash_password = Utils.hashing(password)

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # If account exists show error and validation checks
        account = Database.user_exists_in_db(cursor, mysql, hash_username)
        if account:
            msg = 'Account already exists!'
        elif not Utils.isvalid_email(email):
            msg = 'Invalid email address!'
        elif not Utils.isvalid_username(username):
            msg = 'Username must contain only characters and numbers!'
        elif not Utils.isvalid_password(password):
            msg = 'Invalid password format!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            # cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (hash_username, hash_password, email,))
            # mysql.connection.commit()
            Database.insert_account_record(cursor, mysql, [hash_username, hash_password, email])
            msg = 'Successfully registered'
        # end if
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # end if
    cursor.close()
    print(msg)
    return jsonify(
        msg=msg
    )

# http://localhost:5000/api/register
# this will be the registration page, we need to use both GET and POST requests
@app.route('/api/<username>', methods=['GET', 'POST'])
def update_password(username):
    # Output message if something goes wrong...
    msg = 'No input parameters'
    #register_html = Macros.FRONTEND_DIR / 'register.html'
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and \
       'password' in request.form and \
       'email' in request.form:
        
        # Create variables for easy access
        hash_username = username
        password = request.form['password']
        hash_password = Utils.hashing(password)
        email = request.form['email']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # If account exists show error and validation checks
        account = Database.user_exists_in_db(cursor, mysql, hash_username)
        if account:
            if Utils.isvalid_password(password):
                cursor, mysql, msg = Database.update_password_record(cursor, mysql, [hash_username, hash_password, email])
            else:
                msg = 'Invalid password format!'
            # end if
        else:
            msg = 'Account is not registered'
        # end if
    # end if
    cursor.close()
    print(msg)
    return jsonify(
        msg=msg
    )

@app.route('/api/<username>', methods=['GET', 'POST'])
def grocery(username):
    msg = ''
    stores = None
    # check if the requested location exists
    if request.method == 'POST' and 'city' in request.form:
        msg = 
        # Create variables for easy access
        city = request.form['city']
        state = request.form['state']
        stores = Database.get_stores_exist_in_db(cursor, mysql, [city, state])
        if stores:
            # get store addresses
            # stores = [s[1] for s in stors] 
            msg = 'Successfully store set'
        else:
            msg = 'store not exists'
        # end if
    # end if
    cursor.close()
    return jsonify(
        msg = msg,
        stores = stores
    )
    
def add_item(request):
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and \
       'item' in request.form and \
       'add' in request.form and \
       'store_address' in request.form and \
       'city' in request.form and \
       'state' in request.form:
        
        # Create variables for easy access
        isadd = request.form['add']
        itemname = request.form['item']
        quantity = request.form['quantity']
        store_address = request.form['store_address']
        store_city = request.form['city']
        store_state = request.form['state']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if isadd:
            # Check if item exists using MySQL
            cursor, mysql, msg = Database.add_item_in_db(cursor, mysql, [itemname, quantity, store_address, store_city, store_state])
        else:
            msg = 'Addition failed'
        # end if
        cursor.close()
    # end if    
    return msg

def update_item_quantity(request):
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and \
       'item' in request.form and \
       'update' in request.form and \
       'old_quantity' in request.form and \
       'new_quantity' in request.form and \
       'store_address' in request.form and \
       'city' in request.form and \
       'state' in request.form:
        
        # Create variables for easy access
        isupdate = request.form['update']
        itemname = request.form['item']
        old_quantity = request.form['old_quantity']
        new_quantity = request.form['new_quantity']
        store_address = request.form['store_address']
        store_city = request.form['city']
        store_state = request.form['state']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if isupdate:
            cursor, mysql, msg = Database.update_item_in_db(cursor, mysql, [itemname, old_quantity, new_quantity, store_address, store_city, store_state])
        else:
            msg = 'Update failed'
        # end if
        cursor.close()
    # end if
    return msg

def delete_item(request):
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and \
       'item' in request.form and \
       'delete' in request.form and \
       'store_address' in request.form and \
       'city' in request.form and \
       'state' in request.form:
        
        # Create variables for easy access
        isdelete = request.form['delete']
        itemname = request.form['item']
        quantity = request.form['quantity']
        store_address = request.form['store_address']
        store_city = request.form['city']
        store_state = request.form['state']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if isdelete:
            cursor, mysql, msg = Database.add_item_in_db(cursor, mysql, [itemname, quantity, store_address, store_city, store_state])
        else:
            msg = 'Deletion failed'
        # end if
        cursor.close()
    # end if
    return msg

# Http://localhost:5000/api/<username>/shopping
@app.route('/api/<username>/shopping', methods=['GET', 'POST'])
def items(username):
    obj = None
    msg = ''
    request_type = ''
    if request.method == 'POST' and 'type' in request.form:
        request_type = request.form['type']
        if request_type=='add':
            obj = add_item(request)
        elif request_type=='update':
            obj = update_item_quantity(request)
        elif request_type=='delete':
            obj = delete_item(request)
        # end if
    # end if
    return jsonify(
        request_type=request_type
        msg=msg
    )

# http://localhost:5000/api/<username>/payment
@app.route('/api/<username>/payment', methods=['GET', 'POST'])
def payment(username):
    msg = ''
    # check if the requested location exists
    if request.method == 'POST' and 'city' in request.form:
        msg = 
        # Create variables for easy access
        city = request.form['city']
        state = request.form['state']
        store = Database.store_exists_in_db(cursor, mysql, [city, state])
        if store:
            msg = 'Successfully store set'
        else:
            msg = 'store not exists'
        # end if
    # end if
    cursor.close()
    return jsonify(
        msg = msg
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
