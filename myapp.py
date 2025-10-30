from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = '!@#$%'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'
Mysql = MySQL (app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'iniemail' in request.form and 'inipassword' in request.form:
        email = request.form ['iniemail']
        password = request.form ['inipassword'] 
        cur = Mysql.connection.cursor()
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
        cur = Mysql.connection.cursor()
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

if __name__ == '__main__':
    app.run (debug=True)