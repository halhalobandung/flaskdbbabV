from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = '!@#$%'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'

mysql = MySQL (app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'iniemail' in request.form and 'inipassword' in request.form:
        email = request.form ['iniemail']
        password = request.form ['inipassword'] 
        cur = mysql.connection.cursor()
        cur.execute ("SELECT * FROM users where email = %s and password = %s", (email, password))
        result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect (url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute ("SELECT * FROM users")
        data = cur.fetchall()
        cur.close()
        return render_template('home.html', users=data)
    else:
        return redirect (url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    return redirect(url_for ('login'))

@app.route('/api/create_users', methods=['POST'])
def create_users():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    alamat = data.get('alamat')
    notelp = data.get('notelp')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(username, email, password, alamat, notelp) VALUES(%s, %s, %s, %s, %s)", (username, email, password, alamat, notelp))
    mysql.connection.commit()
    cur.close()
    return jsonify({'massage': 'User created successfully'}), 201

@app.route('/api/get_users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, email, password FROM users")
    users = cur.fetchall()
    cur.close()
    user_list = [{'username': user[0], 'email': user[1], 'password': user[2]} for user in users]
    return jsonify(user_list), 200 

if __name__ == '__main__':
    app.run (debug=True)