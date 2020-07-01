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
adminkey = 'specialkey'
# Componentes para interactuar con la base de datos

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

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM instruments WHERE state = 1')
    data = cur.fetchall()

    return render_template('profile.html', electric_guitar = data)

@app.route('/adminprofile', methods=['GET', 'POST'])
def adminprofile():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('index2'))
    return render_template('adminprofile.html')

@app.route('/adminsignup', methods=['GET', 'POST'])
def adminsignup():
    error = ""
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = request.form["username"]
        special_key = request.form["specialkey"]
        
        users = cur.execute('SELECT username FROM adminusers WHERE username = "'+ username + '"')
        if users >= 1:
            error = '¡Nombre de usuario no disponible!'
            return render_template('adminsignup.html', error = error)

        if special_key == adminkey:
            password = request.form["password"]
            #MySQL request
            cur.execute('INSERT INTO adminusers (username, password) VALUES (%s, %s)', (username, password))
            mysql.connection.commit()
            flash('¡Usuario agregado exitosamente!')
            return render_template('adminsignup.html', error = error)
        error ='Hubo un error insertando los datos'
    return render_template('adminsignup.html', error = error)


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
            if account['state'] == 1:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['iduserlog']
                session['username'] = account['username_userlog']
                return redirect(url_for('profile'))

            else:
                flash('Usuario bloqueado')
                return render_template('login.html')

        flash('Error al introducir los datos')
    return render_template('login.html')


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        special_key = request.form['special_key']
        # Check if account exists using MySQL
        if special_key == adminkey:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM adminusers WHERE username = %s AND password = %s', (username, password))
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('adminprofile'))
            else:
                flash('Error al introducir los datos')
        else:
            flash('Error al introducir los datos')
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
            cur.execute('INSERT INTO userlog (username_userlog, password_userlog, state) VALUES (%s, %s, 1)', (username, password))
            cur.execute('INSERT INTO user_info (user_info_firstname, user_info_secondname, email, user_info_phone, user_info_adress, user_info_country, dateofbirth, user_info_zip, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)', (firstname, lastname, email, phone, address, country, dateofbirth, zip ))
            mysql.connection.commit()
            flash('¡Usuario agregado exitosamente!')
    return render_template('signup.html', error = error)

#Show instruments

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

#CAR COMPONENTS

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
        cur.execute('INSERT INTO car (model, brand, price, photo, type, tipo, stock, hash, tabla, userid, quantity, state, idproduct) SELECT model, brand, price, photo, type, tipo, stock, hash, tabla, ' + str(session['id']) + ', ' + str(cantidad) + ', 1, ' + str(id) + ' FROM ' + ti +' WHERE id = ' + id)
        mysql.connection.commit()
        flash('¡Articulo agregado exitosamente!')

        return redirect(url_for('profile'))

@app.route('/car', methods=['GET', 'POST'])
def car():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car WHERE userid = ' + str(session['id']) + ' AND state = 1')
    data = cur.fetchall()
    cur.execute('SELECT * FROM user_info WHERE id = ' + str(session['id']))
    user = cur.fetchall()
    cont = 0.0
    for x in data:
        cont = cont + (float(x[3]) * float(x[11]))
    iva = cont * 0.12
    totaliva = iva + cont

    cur.execute('SELECT * FROM invoices WHERE iduser = ' + str(session['id']))
    invoices = cur.fetchall()


    return render_template('car.html', car = data, total = cont, iva = iva, totaliva = totaliva, invoices = invoices)

@app.route('/admincar', methods=['GET', 'POST'])
def admincar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car Where state = 1')
    data = cur.fetchall()
    cont = 0.0
    for x in data:
        cont = cont + (float(x[3]) * float(x[11]))
    iva = cont * 0.12
    totaliva = iva + cont

    cur.execute('SELECT * FROM invoices WHERE devolution = 1')
    invoices = cur.fetchall()

    return render_template('admincar.html', car = data, total = cont, iva = iva, totaliva = totaliva, invoices = invoices)

@app.route('/admincardelete/<id>', methods=['GET', 'POST'])
def admincardelete(id):
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

    cur.execute('SELECT model FROM car WHERE id = ' + str(id))
    model = cur.fetchall()

    cur.execute('SELECT userid FROM car WHERE id = ' + str(id))
    userid = cur.fetchall()

    cur.execute('SELECT tabla FROM car WHERE id = ' + str(id))
    tabla = cur.fetchall()

    cur.execute('UPDATE ' + tabla[0][0] + ' SET stock = ' + str(newstock) + ' WHERE id = ' + str(idproduct))
    mysql.connection.commit()

    #¡¡!!!
    cur.execute('UPDATE car SET state = 0 WHERE userid = %s and id = %s', (userid[0][0], id))
    mysql.connection.commit()

    cur.execute('UPDATE car SET stock = ' + str(newstock) +' WHERE userid = %s and id = %s', (str(userid[0][0]), str(id)))
    mysql.connection.commit()

    return redirect(url_for('admincar'))

@app.route('/adminrecovercar/<id>', methods=['GET', 'POST'])
def adminrecovercar(id):

    cur = mysql.connection.cursor()
    #extract product
    #extract the product from products table
    cur.execute('SELECT quantity FROM car WHERE id = ' + str(id))
    stockproduct = cur.fetchall()

    #extract the product from the car
    cur.execute('SELECT stock FROM car WHERE id = ' + str(id))
    stockcar = cur.fetchall()
    #update stock product
    newstock = int(stockcar[0][0]) - int(stockproduct[0][0])

    # extracting product car id
    cur.execute('SELECT idproduct FROM car WHERE id = ' + str(id))
    pid = cur.fetchall()
    idproduct = pid[0][0]

    cur.execute('SELECT model FROM car WHERE id = ' + str(id))
    model = cur.fetchall()

    cur.execute('SELECT userid FROM car WHERE id = ' + str(id))
    userid = cur.fetchall()

    cur.execute('SELECT tabla FROM car WHERE id = ' + str(id))
    tabla = cur.fetchall()

    cur.execute('UPDATE ' + tabla[0][0] + ' SET stock = ' + str(newstock) + ' WHERE id = ' + str(idproduct))
    mysql.connection.commit()

    cur.execute('UPDATE car SET stock = ' + str(newstock) + ' WHERE id = ' + id)
    mysql.connection.commit()
    #¡¡!!!
    cur.execute('UPDATE car SET state = 1 WHERE userid = %s and id = %s', (userid[0][0], id))
    mysql.connection.commit()
    return redirect(url_for('admincar'))


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

    cur.execute('SELECT tabla FROM car WHERE id = ' + str(id))
    tabla = cur.fetchall()

    cur.execute('UPDATE ' + tabla[0][0] + ' SET stock = ' + str(newstock) + ' WHERE id = ' + str(idproduct))
    mysql.connection.commit()

    #update car state
    cur.execute('SELECT * FROM user_info WHERE id = %s', str(session['id']))
    user = cur.fetchall()
    #¡¡!!!
    cur.execute('UPDATE car SET state = 0 WHERE userid = %s and id = %s', (str(user[0][0]), str(id)))
    mysql.connection.commit()

    cur.execute('UPDATE car SET stock = ' + str(newstock) +' WHERE userid = %s and id = %s', (str(user[0][0]), str(id)))
    mysql.connection.commit()
    return redirect(url_for('car'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout(): 

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car WHERE userid = %s and state = 1', str(session['id']))
    data = cur.fetchall()
    cont = 0.0
    for x in data:
        cont = cont + (float(x[3]) * float(x[11]))
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
    cur.execute('''INSERT INTO invoices (hash, iduser, fistname, lastname, expedate, duedate, amount, state, devolution) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
    (str(hash), user[0][0] ,user[0][1], user[0][2], str(today), str(today2), str(totaliva), str(1), str(0)))
    mysql.connection.commit()
    return render_template('invoice.html', car = data, total = cont, iva = iva, totaliva = totaliva, user = user, currentdate = currentdate, duedate = duedate, hash = hash)

#END CAR COMPONENTS

#ADMIN ACTIONS
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


@app.route('/editproduct/<id>', methods=['GET', 'POST'])
def editproduct(id):
   
    cur = mysql.connection.cursor()
    cur.execute('SELECT photo, model, brand, price, stock FROM ' + ti + ' WHERE id = ' + str(id))
    data = cur.fetchall()

    return render_template('editproduct.html', data = data, id = id)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):

    if request.method == 'POST':
        photo = request.form['photo']
        model = request.form['model']
        brand = request.form['brand']
        price = request.form['price']
        stock = request.form['stock']
        cur = mysql.connection.cursor()

        cur.execute('UPDATE '+ ti + ' SET photo = "'+ photo + '"' + ', model = "' + model + '"' + ', brand = "' + brand + '"' + ', price = "' + str(price) + '"' + ', stock = "' + str(stock) + '"' + ' WHERE id = ' + id)
        flash('Producto editado satisfactoriamente!!')
        mysql.connection.commit()
        return redirect(url_for('adminprofile'))


# Users Operations 
@app.route('/adminusers', methods=['GET', 'POST'])
def adminusers():

    cur = mysql.connection.cursor()
    #consulting userlog
    cur.execute('SELECT * FROM userlog ')
    userlog = cur.fetchall()
    cur.execute('SELECT user_info_firstname, user_info_secondname, email, user_info_phone, user_info_country, user_info_adress, state, id FROM user_info')
    userinfo = cur.fetchall()

    return render_template('adminusers.html', userlog = userlog, userinfo = userinfo)


@app.route('/deleteuser/<id>', methods=['GET', 'POST'])
def deleteuser(id):

    print('')
    print('')
    print(type(id))
    print('')
    print('')
    cur = mysql.connection.cursor()
    cur.execute('UPDATE userlog SET state = 0 WHERE iduserlog = '+ id )
    mysql.connection.commit()
    cur.execute('UPDATE user_info SET state = 0 WHERE id = ' + id )
    mysql.connection.commit()
    return redirect(url_for('adminusers'))


@app.route('/recoveruser/<id>', methods=['GET', 'POST'])
def recoveruser(id):

    cur = mysql.connection.cursor()
    #consulting userlog
    cur.execute('UPDATE userlog SET state = 1 WHERE iduserlog = ' + id)
    mysql.connection.commit()
    cur.execute('UPDATE user_info SET state = 1 WHERE id = ' + id )
    mysql.connection.commit()
    return redirect(url_for('adminusers'))


@app.route('/profilesearch', methods=['GET', 'POST'])
def profilesearch():

    if request.method == "POST":

        search = request.form["search"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM instruments WHERE model LIKE '%" + search + "%'" + " OR brand LIKE '%" + search + "%'" )
        data = cur.fetchall()
        return render_template('profile.html', electric_guitar = data)

@app.route('/profilesearch2', methods=['GET', 'POST'])
def profilesearch2():
    if request.method == "POST":

        search = request.form["search"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM instruments WHERE model LIKE '%" + search + "%'" + " OR brand LIKE '%" + search + "%'" )
        data = cur.fetchall()
        return render_template('adminprofile.html', electric_guitar = data)

@app.route('/carsearch', methods=['GET', 'POST'])
def carsearch():
    if request.method == "POST":

        search = request.form["search"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM car WHERE model LIKE '%" + search + "%'" + " OR brand LIKE '%" + search + "%'" + " OR state LIKE '%" + search + "%'" + " OR userid LIKE '%" + search + "%'" )
        data = cur.fetchall()
        return render_template('admincar.html', car = data)

@app.route('/usersearch', methods=['GET', 'POST'])
def usersearch():
    if request.method == "POST":

        search = request.form["search"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_info_firstname, user_info_secondname, email, user_info_phone, user_info_country, user_info_adress, state, id  FROM user_info WHERE user_info_firstname LIKE '%" + search + "%'" + " OR user_info_secondname LIKE '%" + search + "%'" + " OR user_info_country LIKE '%" + search + "%'" + " OR user_info_country LIKE '%" + search + "%'" )
        data = cur.fetchall()
        return render_template('adminusers.html', userinfo = data)

@app.route('/devolution/<id>', methods=['GET', 'POST'])
def devolution(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE invoices SET devolution = 1 WHERE id = " + id )
    mysql.connection.commit()
    return redirect(url_for("car"))


@app.route('/aprov/<id>', methods=['GET', 'POST'])
def aprov(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE invoices SET devolution = 1, state = 0 WHERE id = " + id )
    mysql.connection.commit()
    return redirect(url_for("inv"))


@app.route('/inv', methods=['GET', 'POST'])
def inv():
    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM invoices WHERE devolution = 0')
    inv = cur.fetchall()

    cur.execute('SELECT * FROM invoices WHERE devolution = 1')
    invoices = cur.fetchall()

    cur.execute('''SELECT * FROM invoices WHERE expedate > NOW() - INTERVAL 30 DAY
                AND expedate < NOW() + INTERVAL 30 DAY AND devolution = 0 ''')

    mes = cur.fetchall()

    cont2 = 0.0
    for x in mes:
        cont2 = cont2 + (float(x[7]))
   

    return render_template('inv.html', invoices = invoices, inv = inv, mes = mes, t =cont2)


@app.route('/invsearch', methods=['GET', 'POST'])
def invsearch():
    if request.method == "POST":
        search = request.form["search"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM invoices WHERE hash LIKE '%" + search + "%'" + " OR fistname LIKE '%" + search + "%'" + " OR lastname LIKE '%" + search + "%'" + " OR expedate LIKE '%" + search + "%'"+ " OR duedate LIKE '%" + search + "%'" )
        data = cur.fetchall()

        cur.execute('SELECT * FROM invoices WHERE devolution = 1')
        invoices = cur.fetchall()
        return render_template('inv.html', inv = data, invoices = invoices)


@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':

        photo = request.form['photo']
        model = request.form['model']
        brand = request.form['brand']
        price = request.form['price']
        stock = request.form['stock']
        categoria = request.form['categoria']
        cur = mysql.connection.cursor()
        
        cur.execute('''INSERT INTO instruments (model, brand, price, photo, 
                        type, tipo, stock, hash, tabla, state)
                        VALUES(%s, %s, %s, %s, 1, 'nuevo_instrumento', %s, %s, %s, 1)
                    '''
        , (model, brand, price, photo, stock, str(random.randint(0000000, 9999999)), categoria))


        cur.execute('''INSERT INTO ''' + categoria + ''' (model, brand, price, photo, 
                        type, tipo, stock, hash, tabla, state)
                        VALUES(%s, %s, %s, %s, 1, 'nuevo_instrumento', %s, %s, %s, 1)
                    '''
        , (model, brand, price, photo, stock, str(random.randint(0000000, 9999999)), categoria))

        mysql.connection.commit()
        flash('¡Producto añadido exitosamente!')

        print('')
        print('')
        print(categoria)
        print('')
        print('')

        return render_template('/add.html')
    return render_template('/add.html')





if __name__ == '__main__':
    app.run(port=3000, debug=True)

