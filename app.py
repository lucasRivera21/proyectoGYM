from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql, hashlib
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'prueba'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exitoso', methods=['POST'])
def exitoso():
    if request.method == 'POST':
        nombre = request.form['name']
        apellido = request.form['lastname']
        ID = request.form['ID']
        edad = request.form['age']
        correo = request.form['email']
        password = generate_password_hash(request.form['password'])
        admin = 0
        cur = mysql.get_db().cursor()
        query = 'INSERT INTO tabla_prueba (nombre, apellido, ID, edad, correo, password, admin) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cur.execute(query, (nombre, apellido, ID, edad, correo, password, admin))
        cur.close()
        return render_template('exitoso.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        cur = mysql.get_db().cursor()
        query = "SELECT correo, password, nombre, admin, apellido FROM tabla_prueba WHERE correo = '{}'".format(request.form['email'])
        cur.execute(query)
        global row
        row = cur.fetchone()
        cur.close()
        if row != None:
            if check_password_hash(row[1], request.form['password']):
                if row[3] == '1':
                    return redirect(url_for('super'))
                else:
                    return redirect(url_for('usuario'))
        else:
            print("No hay")
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/usuario')
def usuario():
    return render_template('usuarioNormal.html', name=row[2], password=row[1], apellido=row[4])

@app.route('/super', methods=['POST', 'GET'])
def super():
    cur = mysql.get_db().cursor()
    query = "SELECT nombre, apellido, ID, edad, correo FROM tabla_prueba WHERE admin = '0'"
    cur.execute(query)
    global datos
    datos = cur.fetchall()
    cur.close()
    return render_template('superUsuario.html', name=row[2], datos=datos)

@app.route('/borrar', methods=['POST'])
def borrar():
    if request.method == 'POST':
        DU = int(request.form['btn-borrar'])-1
        cur = mysql.get_db().cursor()
        query = "DELETE FROM tabla_prueba WHERE ID = '{}'".format(datos[DU][2])
        cur.execute(query)
        cur.close()
        return redirect(url_for('super'))

@app.route('/editar', methods=['POST'])
def editar():
    if request.method == 'POST':
        print(request.form['btn-editar'])
    return redirect(url_for('super'))

@app.route('/registro-super', methods=['POST', 'GET'])
def registroSuper():
    if request.method == 'POST':
        cur = mysql.get_db().cursor()
        query= "SELECT correo, admin FROM tabla_prueba WHERE correo ='{}'".format(request.form['correoAdmin'])
        cur.execute(query)
        adminDb = cur.fetchone()
        if adminDb != None and adminDb[1] == '1':
            print(adminDb)
            passwordAdmin = generate_password_hash(request.form['passwordAdmin'])
            query = "UPDATE tabla_prueba set password = '{}' WHERE correo='{}'".format(passwordAdmin, adminDb[0])
            cur.execute(query)
            cur.close()
            return redirect(url_for('superExitoso'))
        else:
            print("No entres")
            cur.close()
            return redirect(url_for('superFallido'))
    else:
        return render_template('registroSuper.html')
@app.route('/superExitoso')
def superExitoso():
    return render_template('exitosoSuper.html')

@app.route('/superFallido')
def superFallido():
    return render_template('fallidoSuper.html')

if __name__ == '__main__':
    app.run(debug=True)
