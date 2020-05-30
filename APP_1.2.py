from flask import Flask
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
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


@app.route('/index2', methods=['GET', 'POST'])
def index2():
    return render_template('index2.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO userlog (username_userlog, password_userlog) VALUES (%s, %s)',
                    (username, password))
        mysql.connection.commit()
        flash('Usuario Añadido exitosamente!')

    return render_template('signup.html')

@app.route('/showinstruments/<string:tipo>/', methods=['GET', 'POST'])
def show(tipo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM {0}' .format(tipo))
    data = cur.fetchall()
    global ti
    ti = tipo
    return render_template('profile.html', electric_guitar = data)

@app.route('/showinstruments2/<string:tipo>/', methods=['GET', 'POST'])
def show2(tipo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM {0}' .format(tipo))
    data = cur.fetchall()
    global ti
    ti = tipo
    return render_template('index2.html', electric_guitar = data)
    

@app.route('/addtocar/<id>', methods=['GET', 'POST'])
def addtocar(id):
    
    cur = mysql.connection.cursor()
    print(ti)
    cur.execute('INSERT INTO car (model, brand, price, photo, type, tipo, userid) SELECT model, brand, price, photo, type, tipo, ' + str(session['id']) + ' FROM ' + ti +' WHERE id= ' + str(id))
    mysql.connection.commit()
    flash('¡Articulo agregado exitosamente!')
    return redirect(url_for('profile'))


@app.route('/car', methods=['GET', 'POST'])
def car():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car WHERE userid = %s', str(session['id']))
    data = cur.fetchall()
    return render_template('car.html', car = data)

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
