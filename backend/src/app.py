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
                data=Utils.hashing(username, password)
            )
        # end if
    # end if
    msg = 'Incorrect username/password!'
    return jsonify(
        msg=msg
    )


# http://localhost:5000/egrocerycart/logout
# This will be the logout page
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
# this will be the registration page, we need to use both GET and POST requests
@app.route('/egrocerycart/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    register_html = Macros.FRONTEND_DIR / 'register.html'
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
            msg = 'You have successfully registered!'
        # end if
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # end if
    return jsonify(
        msg=msg
    )


# # http://localhost:5000/egrocerycart/home
# # This will be the home page, only accessible for loggedin users
# @app.route('/egrocerycart/home')
# def home():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         home_html = Macros.FRONTEND_DIR / 'home.html'
#         # User is loggedin show them the home page
#         return render_template(str(home_html), username=session['username'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))


# # http://localhost:5000/egrocerycart/profile
# # This will be the profile page, only accessible for loggedin users
# @app.route('/egrocerycart/profile')
# def profile():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         profile_html = Macros.FRONTEND_DIR / 'profile.html'
#         # We need all the account info for the user so we can display it on the profile page
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
#         account = cursor.fetchone()
#         # Show the profile page with account info
#         return render_template(str(profile_html), account=account)
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))


