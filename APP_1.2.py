from flask import Flask
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, send_file, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from tempfile import NamedTemporaryFile
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
import os
from InvoiceGenerator.pdf import SimpleInvoice
from datetime import date, timedelta
import random
#from flask_login import *

# Coneeccion mysql
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Morfologia123'
app.config['MYSQL_DB'] = 'store1'
mysql = MySQL(app)

# SESSION
app.secret_key = 'mysecretkey'
ti = ""
# Componentes para interactuar con la base de datos

'''
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM userlog')
    data = cur.fetchall()
    return render_template("index.html", contacts=data)
'''

'''
@app.route('/add_contact', methods = ['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', 
        (fullname, phone, email)) 
        mysql.connection.commit()
        flash('Contact added sussesfully')
        return redirect(url_for('index'))

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
                email = %s,
                phone = %s
                WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit_contact(id):
     cur = mysql.connection.cursor()
     cur.execute('SELECT * FROM contacts WHERE id = %s',(id))
     data = cur.fetchall()
     return render_template('edit.html', contact = data[0])

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}' .format(id))
    mysql.connection.commit()
    flash('Contact removed successfully')
    return redirect(url_for('index'))

'''

# Rutas para el registro de usuario signuplogin


@app.route('/signup_login')
def user_register():
    if request.method == 'POST':
        if request.form['login'] == 'Registrarse':
            pass
        elif request.form['sign up'] == 'Entrar':
            pass  # do something else
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('signup_login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('index2'))
    return render_template('profile.html')

@app.route('/adminprofile', methods=['GET', 'POST'])
def adminprofile():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('index2'))
    return render_template('adminprofile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM userlog WHERE username_userlog = %s AND password_userlog = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['iduserlog']
            session['username'] = account['username_userlog']
            return redirect(url_for('profile'))
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM userlog WHERE username_userlog = %s AND password_userlog = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['iduserlog']
            session['username'] = account['username_userlog']
            return redirect(url_for('profile'))
        return redirect(url_for('adminlogin'))
    return render_template('adminlogin.html')

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    return render_template('index2.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = request.form["username"]
        users = cur.execute('SELECT username_userlog FROM userlog WHERE username_userlog = "'+ username + '"')
        if users >= 1:
            error = '¡Nombre de usuario no disponible!'
        else:
            password = request.form["password"]
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            email = request.form["email"]
            phone = request.form["phone"]
            address = request.form["address"]
            country = request.form["country"]
            dateofbirth = request.form["dateofbirth"]
            zip = request.form["zip"]
            #MySQL request
            cur.execute('INSERT INTO userlog (username_userlog, password_userlog) VALUES (%s, %s)', (username, password))
            cur.execute('INSERT INTO user_info (user_info_firstname, user_info_secondname, email, user_info_phone, user_info_adress, user_info_country, dateofbirth, user_info_zip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (firstname, lastname, email, phone, address, country, dateofbirth, zip ))
            mysql.connection.commit()
    return render_template('signup.html', error = error)


@app.route('/showinstruments/<string:tipo>/', methods=['GET', 'POST'])
def show(tipo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM {0} WHERE state = 1' .format(tipo))
    data = cur.fetchall()
    global ti
    ti = tipo
    return render_template('profile.html', electric_guitar = data)


@app.route('/showinstruments2/<string:tipo>/', methods=['GET', 'POST'])
def show2(tipo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM {0} WHERE state = 1' .format(tipo))
    data = cur.fetchall()
    global ti
    ti = tipo
    return render_template('index2.html', electric_guitar = data)

#Admin
@app.route('/showinstrumentst/<string:tipo>/', methods=['GET', 'POST'])
def show3(tipo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM {0} ' .format(tipo))
    data = cur.fetchall()
    global ti
    ti = tipo
    return render_template('adminprofile.html', electric_guitar = data)    

@app.route('/addtocar/<id>', methods=['GET', 'POST'])
def addtocar(id):
    
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cantidad = request.form['quantity']
        
        #extract the product
        cur.execute('SELECT stock FROM ' + ti + ' WHERE id = ' + str(id))
        product = cur.fetchall()
        newstock = int(product[0][0]) - int(cantidad)
        
        #update stock
        cur.execute('UPDATE ' + ti + ' SET stock = ' + str(newstock) + ' WHERE id = ' + str(id))
        mysql.connection.commit()

        #insert into car
        cur.execute('INSERT INTO car (model, brand, price, photo, type, tipo, stock, hash, userid, quantity, state, idproduct) SELECT model, brand, price, photo, type, tipo, stock, hash, ' + str(session['id']) + ', ' + str(cantidad) + ', 1, ' + str(id) + ' FROM ' + ti +' WHERE id = ' + str(id))
        mysql.connection.commit()
        flash('¡Articulo agregado exitosamente!')

        return redirect(url_for('profile'))


@app.route('/car', methods=['GET', 'POST'])
def car():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car WHERE userid = %s AND state = 1', str(session['id']))
    data = cur.fetchall()
    cur.execute('SELECT * FROM user_info WHERE id = %s', str(session['id']))
    user = cur.fetchall()
    cont = 0.0
    for x in data:
        cont = cont + (float(x[3]) * float(x[9]))
    iva = cont * 0.12
    totaliva = iva + cont
    return render_template('car.html', car = data, total = cont, iva = iva, totaliva = totaliva)

@app.route('/admincar', methods=['GET', 'POST'])
def admincar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car')
    data = cur.fetchall()
    cont = 0.0
    for x in data:
        cont = cont + (float(x[3]) * float(x[9]))
    iva = cont * 0.12
    totaliva = iva + cont
    return render_template('admincar.html', car = data, total = cont, iva = iva, totaliva = totaliva)

@app.route('/cardelete/<id>', methods=['GET', 'POST'])
def cardelete(id):
    cur = mysql.connection.cursor()

    #extract product
    #extract the product from products table
    cur.execute('SELECT quantity FROM car WHERE id = ' + str(id))
    stockproduct = cur.fetchall()

    #extract the product from the car
    cur.execute('SELECT stock FROM car WHERE id = ' + str(id))
    stockcar = cur.fetchall()
    #update stock product
    newstock = int(stockproduct[0][0]) + int(stockcar[0][0])

    # extracting product car id
    cur.execute('SELECT idproduct FROM car WHERE id = ' + str(id))
    pid = cur.fetchall()
    idproduct = pid[0][0]

    cur.execute('UPDATE ' + ti + ' SET stock = ' + str(newstock) + ' WHERE id = ' + str(idproduct))
    mysql.connection.commit()

    #update car state
    cur.execute('SELECT * FROM user_info WHERE id = %s', str(session['id']))
    user = cur.fetchall()
    #¡¡!!!
    cur.execute('UPDATE car SET state = 0 WHERE userid = %s and id = %s', (str(user[0][0]), str(id)))
    mysql.connection.commit()


    return redirect(url_for('car'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout(): 

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car WHERE userid = %s and state = 1', str(session['id']))
    data = cur.fetchall()
    cont = 0.0
    for x in data:
        cont = cont + (float(x[3]) * float(x[9]))
    iva = cont * 0.12
    totaliva = iva + cont
    cur.execute('SELECT * FROM user_info WHERE id = %s', str(session['id']))
    user = cur.fetchall()
    #date now
    today = date.today()
    # dd/mm/YY
    currentdate = today.strftime("%d/%m/%Y")
    today2 = today + timedelta(days=30)
    duedate = today2.strftime("%d/%m/%Y")
    hash = random.getrandbits(16)

    #consulta para eliminacion logica del carrito
    cur.execute('UPDATE car SET state = %s WHERE userid = %s', (str(0), str(user[0][0])))
    mysql.connection.commit()

    #invoices
    cur.execute('''INSERT INTO invoices (hash, iduser, fistname, lastname, expedate, duedate, amount, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
    (str(hash), user[0][0] ,user[0][1], user[0][2], str(today), str(today2), str(totaliva), str(1) ))
    mysql.connection.commit()
    return render_template('invoice.html', car = data, total = cont, iva = iva, totaliva = totaliva, user = user, currentdate = currentdate, duedate = duedate, hash = hash)

#Admin
@app.route('/admindelete/<id>')
def admindelete(id):
    cur = mysql.connection.cursor()
    #Delete instrument by logical elimination
    cur.execute('SELECT idproduct FROM car WHERE id = ' + str(id))
    pid = cur.fetchall()

    cur.execute('UPDATE ' + ti + ' SET state = 0 WHERE id = ' + str(id))
    mysql.connection.commit()

    # Refresh the car
    # Product consult inside car.html
    
    cur.execute('SELECT hash FROM ' + ti + ' WHERE id = ' + str(id))
    hash = cur.fetchall()
    #Update de db with logical elimination
    cur.execute('UPDATE car SET state = 0 WHERE hash = ' + str(hash[0][0]) )
    mysql.connection.commit()

    flash('Elemento eliminado con exito')

    return redirect(url_for('adminprofile'))



@app.route('/adminrecover/<id>')
def adminrecover(id):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE ' + ti + ' SET state = 1 WHERE id = ' + str(id))
    mysql.connection.commit()

    #consulting hash
    cur.execute('SELECT hash FROM ' + ti + ' WHERE id = ' + str(id))
    hash = cur.fetchall()
    #Update de db with logical elimination
    cur.execute('UPDATE car SET state = 1 WHERE hash = ' + str(hash[0][0]) )
    mysql.connection.commit()


    flash('Elemento recuperado con exito con exito')
    return redirect(url_for('adminprofile'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)


    '''
@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        # En la session Debe haber un formulario que la cierre, para no entrar a ella si
        # se intento entrar anteriormente   
        #user = [x for x in users if x.username == username][0]
        user = None
        for x in users:
            if x.username == username:
                user = x  
        if user != None and user.username == username and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        return redirect(url_for('login'))
    return render_template('login.html')
'''

# Componente auxiliar para el inicio de session, verifica si hay usuario
# @app.before_request
# def before_request():
#    if 'user_id' in session:
#        user = [x for x in users if x.id == session['user_id']][0]
#        g.user = user
#    else:
#        g.user = None

# Creacion del objeto usuario, este es para hacer pruebas luego se incluira la base de datos

#                 LOGIN MANAGER
'''
login_manager = LoginManager()
login_manager.init_app(app)
'''
'''
@app.route('/', methods = ['POST'])
def log_out():
    if (request.form['log_out'] == 'log_out'):
        session.pop('username', None)
    return redirect(url_for('index2'))

#if (request.form['log_out'] == 'log_out'):
    #    session.pop('username', None)
    #    return redirect(url_for('login'))

'''
