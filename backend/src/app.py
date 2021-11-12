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
        username = Utils.hashing(username)
        password = Utils.hashing(password)
        
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

# http://localhost:5000/egrocerycart/register
@app.route('/egrocerycart/shopping', methods=['GET', 'POST'])
def add_item():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and \
       'item' in request.form and \
       'add' in request.form:
        
        # Create variables for easy access
        isadd = request.form['add']
        store_loc = request.form['location']
        itemname = request.form['item']
        quantity = request.form['quantity']

        if isadd:
            # Check if item exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM items WHERE location = %s AND itemname = %s AND quantity >= %s',
                (store_loc, itemname, quantity)
            )
            isavail = cursor.fetchone()
            if isavail:
                cursor.execute(
                    'UPDATE items SET quantity = quantity - %s WHERE location = %s AND itemname = %s',
                    (quantity, store_loc, itemname)
                )
                mysql.connection.commit()
                msg = 'Successfully added'
            else:
                msg = 'Item is not available'
            # end if
        else:
            msg = 'Addition failed'
        # end if
    # end if    
    return jsonify(
        msg=msg
    )

# http://localhost:5000/egrocerycart/register
@app.route('/api/shopping', methods=['GET', 'POST'])
def delete_item():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and \
       'item' in request.form and \
       'delete' in request.form:
        
        # Create variables for easy access
        isdelete = request.form['delete']
        store_loc = request.form['location']
        itemname = request.form['item']
        quantity = request.form['quantity']

        if isdelete:
            # Check if item exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM items WHERE location = %s AND itemname = %s',
                (store_loc, itemname)
            )
            isavail = cursor.fetchone()
            if isavail:
                # Check if item exists using MySQL
                cursor.execute(
                    'UPDATE items SET quantity = quantity + %s WHERE location = %s AND itemname = %s',
                    (quantity, store_loc, itemname)
                )
                mysql.connection.commit()
            else:
                cursor.execute(
                    'INSERT INTO items (location, itemname, quantity) VALUES (%s, %s, %s)',
                    (store_loc, itemname, quantity)
                )
            # end if
            msg = 'Successfully deleted'
        else:
            msg = 'Deletion failed'
        # end if
    # end if
    return jsonify(
        msg=msg
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
