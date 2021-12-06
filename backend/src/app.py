from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from macros import Macros
from utils import Utils
from database import Database

import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = Macros.SECRETE_KEY

# DB connection details
app.config['MYSQL_HOST'] = Macros.MYSQL_HOST
app.config['MYSQL_USER'] = Macros.MYSQL_USER
# app.config['MYSQL_PASSWORD'] = Macros.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Macros.MYSQL_DB #str(Macros.DB_FILE)

mysql = MySQL(app)
Macros.DB_DIR.mkdir(parents=True, exist_ok=True)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@cross_origin()

@app.route("/api/status", methods=['GET'])
def status():
  return "running"

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    # test username: jasonlee123
    # test password: Password2021!@
    # test email: jxl115330@abc.com
    msg = ''
    code = 500
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
            session['username'] = username
            code = 200
            msg = "Successfully logged in!"
        else:
            msg = 'Incorrect username/password!'
        # end if
        cursor.close()
    # end if
    print(msg)
    return jsonify(
        code=code,
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
    print(msg)
    return jsonify(
        msg=msg
    )

# http://localhost:5000/api/register
# this will be the registration page, we need to use both GET and POST requests
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = 'No input parameters'
    code = 400
    # register_html = Macros.FRONTEND_DIR / 'register.html'
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
            code = 200
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            # cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (hash_username, hash_password, email,))
            # mysql.connection.commit()
            Database.insert_account_record(cursor, mysql, [hash_username, hash_password, email])
            msg = 'Successfully registered'
        # end if
        cursor.close()
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # end if
    print(msg)
    return jsonify(
        code=code,
        msg=msg
    )

@app.route('/api/profile', methods=['GET', 'POST'])
def profile():
    msg = 'No input parameters'
    if session['loggedin'] and request.method == 'POST':
        userid = session['id']
        username = session['username']
        hash_username = Utils.hashing(username)
        account = Database.user_exists_in_db(cursor, mysql, hash_username)
        if account:
            return jsonify(
                msg=msg,
                account=account
            )
        # end if
    # end if
    return jsonify(
        msg=msg
    )

# http://localhost:5000/api/register
# this will be the registration page, we need to use both GET and POST requests
@app.route('/api/profile/updatepassword', methods=['GET', 'POST'])
def update_password():
    # Output message if something goes wrong...
    msg = 'No input parameters'
    #register_html = Macros.FRONTEND_DIR / 'register.html'
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if session['loggedin'] and \
       request.method == 'POST' and \
       'current_password' in request.form and \
       'new_password' in request.form and \
       'retype_password' in request.form:
        
        # Create variables for easy access
        hash_username = Utils.hashing(session['username'])
        cur_password = request.form['cur_password']
        new_password = request.form['new_password']
        retype_password = request.form['retype_password']
        hash_cur_password = Utils.hashing(cur_password)
        hash_new_password = Utils.hashing(new_password)
        hash_retype_password = Utils.hashing(retype_password)
        email = request.form['email']

        if hash_new_password!=hash_retype_password:
            msg = "New password is not same as retype password"
        elif hash_cur_password == hash_new_password:
            msg = "New password is same as current password"
        else:
            if Utils.isvalid_password(password):
                # Check if account exists using MySQL
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                
                # If account exists show error and validation checks
                account = Database.user_exists_in_db(cursor, mysql, hash_username)
                if account:
                    cursor, mysql, msg = Database.update_password_record(cursor, mysql, [hash_username, hash_password, email])
                else:
                    msg = 'New password is set'
                # end if
                cursor.close()
            else:
                msg = 'Invalid password format!'
            # end if
        # end if
    # end if
    print(msg)
    return jsonify(
        msg=msg
    )

@app.route('/api/profile/stores', methods=['GET', 'POST'])
def stores():
    msg = ''
    stores = None
    # check if the requested location exists
    if session['loggedin'] and \
       request.method == 'POST' and \
       'city' in request.form:
        # Create variables for easy access
        city = request.form['city']
        state = request.form['state']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        stores = Database.get_all_stores_in_db(cursor, mysql)
        if stores:
            msg = 'Successfully stores scanned'
        else:
            msg = 'store not exists'
        # end if
        cursor.close()
    # end if
    print(msg)
    return jsonify(
        msg = msg,
        stores = stores
    )

@app.route('/api/profile/store-change', methods=['GET', 'POST'])
def store_change():
    msg = ''
    stores = None
    # check if the requested location exists
    if session['loggedin'] and \
       request.method == 'POST' and \
       'city' in request.form:
        # Create variables for easy access
        city = request.form['city']
        state = request.form['state']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        stores = Database.get_stores_exist_in_db(cursor, mysql, [city, state])
        if stores:
            # get store addresses
            # stores = [s[1] for s in stors]
            session['store_address'] = stores["address"]
            session['store_city'] = city
            session['store_state'] = state
            msg = 'Successfully store set'
        else:
            msg = 'store not exists'
        # end if
        cursor.close()
    # end if
    print(msg)
    return jsonify(
        msg = msg,
        stores = stores
    )

def add_item(itemcode, quantity, store_address, store_city, store_state):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor, mysql, msg, item_name, item_price = Database.add_item_order(
        cursor, mysql, [itemcode, quantity, store_address, store_city, store_state]
    )
    cursor.close()
    return msg, item_name, item_price

# Http://localhost:5000/api/profile/shopping
@app.route('/api/profile/shopping', methods=['GET', 'POST'])
def scan_item():
    msg = ''
    item_name=''
    if session['loggedin'] and \
       session['store_address'] is not None and \
       session['store_city'] is not None and \
       session['store_state'] is not None and \
       request.method == 'POST' and \
       'itemcode' in request.form:
        username = session['username']
        itemcode = request.form['itemcode']
        store_address = session['store_address']
        store_city = session['store_city']
        store_state = session['store_state']
        msg, item_name, item_price = add_item(
            itemcode, 1, store_address, store_city, store_state
        )
    # end if
    print(msg)
    return jsonify(
        itemname=item_name,
        itemprice=item_price,
        msg=msg
    )

def update_item(
        itemcode,
        prev_quantity, new_quantity,
        prev_total_price,
        store_address, store_city, store_state):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor, mysql, msg, item_name, item_price, new_total_price = Database.update_item_order(
        cursor, mysql, [
            itemcode, prev_quantity, new_quantity, prev_total_price,
            store_address, store_city, store_state
        ]
    )
    cursor.close()
    return msg, item_name, item_price, new_total_price

@app.route('/api/profile/shopping', methods=['GET', 'POST'])
def edit_item():
    msg = ''
    if session['loggedin'] and \
       session['store_address'] is not None and \
       session['store_city'] is not None and \
       session['store_state'] is not None and \
       request.method == 'POST' and \
       'itemcode' in request.form and \
       'prev_quantity' in request.form and \
        'new_quantity' in request.form and \
        'prev_total_price' in request.form:
        username = session['username']
        itemcode = request.form['itemcode']
        prev_quantity = request.form['prev_quantity']
        new_quantity = request.form['new_quantity']
        prev_total_price = request.form['prev_total_price']
        msg, item_name, item_price, new_total_price = update_item(
            itemcode, prev_quantity, new_quantity, prev_total_price,
            store_address, store_city, store_state
        )
    # end if
    print(msg)
    return jsonify(
        itemname=item_name,
        itemprice=item_price,
        total=new_total_price,
        msg=msg
    )

# http://localhost:5000/api/<username>/payment
@app.route('/api/payment', methods=['GET', 'POST'])
def payment():
    msg = ''
    if session['loggedin'] and \
       request.method == 'POST' and \
       'card_number' in request.form and \
       'exp_date' in request.form and \
       'security_code' in request.form:    

        card_number = request.form['card_number']
        exp_date = request.form['exp_date']
        security_code = request.form['security_code']
        invalid_elem = list()
        if not Utils.isvalid_card_number(card_number):
            invalid_elem.append('Card number')
        # end if

        if not Utils.isvalid_exp_date(exp_date):
            invalid_elem.append("Expiration date")
        # end if

        if not Utils.isvalid_sec_code(security_code):
            invalid_elem.append("Security code")
        # end if
        
        if len(invalie_elem)==0:
            msg = 'Valid payment info entered'
            # pop the store selected when the shopping is done
            session.pop('store_address', None)
            session.pop('store_city', None)
            session.pop('store_state', None)
        else:
            msg = "Invalid " + ",".join(invalid_elem) + " info entered"
        # end if
    # end if
    return jsonify(
        msg = msg
    )


# http://localhost:5000/api/<username>/payment
@app.route('/api/orders', methods=['GET', 'POST'])
def orders():
    msg = ''
    if session['loggedin'] and \
       request.method == 'POST' and \
       'item_list' in request.form and \
       'order_type' in request.form:

        item_list = request.form['item_list'] # List of tuples (itemname, quantity)
        order_type = request.form['order_type']
        total_price = request.form['price']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if order_type=="pickup":
            est_wait_time = "10min"
            cursor, mysql, msg = Database.insert_order_record(
                cursor, mysql,
                [username, item_list, order_type, total_price]
            )
        elif order_type=="delivery":
             address = request.form['address']
             shipping_method = request.form['shipping_method']
             cursor, mysql, msg = Database.insert_order_record(
                 cursor, mysql,
                 [username, item_list, order_type, total_price, address, shipping_method]
             )
        # end if
        cursor.close()
    # end if
    return jsonify(
        msg = msg
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
