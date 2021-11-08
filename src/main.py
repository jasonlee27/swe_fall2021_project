from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

from macros import Macros

import MySQLdb.cursors
import re



app = Flask(__name__)

app.secret_key = Macros.SECRETE_KEY

# DB connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'grocerycart_db'

mysql = MySQL(app)

@app.route('/egrocerycart/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    index_html = Macros.FRONTEND_DIR / 'index.html'
    if request.method =='POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

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
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        # end if
    # end if
    return render_template(str(index_html), msg='')


# http://localhost:5000/egrocerycart/logout
# This will be the logout page
@app.route('/egrocerycart/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


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
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template(str(register_html), msg=msg)


