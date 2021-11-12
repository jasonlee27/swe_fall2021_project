from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_mysqldb import MySQL

from macros import Macros
from utils import Utils
from database import Database

import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = Macros.SECRETE_KEY

# DB connection details
app.config['MYSQL_HOST'] = Macros.MYSQL_HOST
app.config['MYSQL_USER'] = Macros.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Macros.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Macros.MYSQL_DB

mysql = MySQL(app)


@app.route('/egrocerycart/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method =='POST' and \
       'username' in request.form and \
       'password' in request.form:
        username = Utils.hashing(request.form['username'])
        password = Utils.hashing(request.form['password'])
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))

        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            return jsonify(
                msg="Successfully logged in"
            )
        # end if
    # end if
    msg = 'Incorrect username/password!'
    return jsonify(
        msg=msg
    )

# http://localhost:5000/egrocerycart/logout
@app.route('/egrocerycart/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    
    msg = 'Successfully logged out'
    return jsonify(
        msg=msg
    )

# http://localhost:5000/egrocerycart/register
@app.route('/egrocerycart/register', methods=['GET', 'POST'])
def register():
    msg = ''
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
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (hash_username,))        
        account = cursor.fetchone()
        
        # If account exists show error and validation checks
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
@app.route('/egrocerycart/shopping', methods=['GET', 'POST'])
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
