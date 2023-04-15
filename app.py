from flask import Flask, render_template, url_for, flash, session, request, redirect, make_response
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'deepak_behera'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
CORS(app)

DB_HOST = 'localhost'
DB_NAME = 'login_logout'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                       password=DB_PASSWORD, host=DB_HOST)

cursor = conn.cursor()
global COOKIE_TIME_OUT
# COOKIE_TIME_OUT = 60*60*24*7 #7 days
COOKIE_TIME_OUT = 60*5  # 5 minutes


@app.route('/')
def index():
    if 'email' in session:
        username = session['email']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>Click here to logout</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + "click here to login</b></a>"


@app.route('/login')
def login():
    return render_template('login_logout_with_rememberme.html')


@app.route('/submit', methods=['POST'])
def login_submit():
    
    with conn:
        with conn.cursor() as cursor:
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']
            _remember = request.form.getlist('inputRemember')

            if 'email' in request.cookies:
                username = request.cookies.get('email')
                password = request.cookies.get('pwd')                
                sql = "SELECT * FROM user_test_flask WHERE email=%s"
                sql_where = (username,)
                cursor.execute(sql, sql_where)
                row = cursor.fetchone()
                if row and check_password_hash(row[4], password):
                    print(username + ' ' + password)
                    session['email'] = row[3]                                        
                    return redirect('/')
                else:
                    return redirect('/login')
            # validate the received values
            elif _email and _password:
                # check user exists            
                sql = "SELECT * FROM user_test_flask WHERE email=%s"
                sql_where = (_email,)
                cursor.execute(sql, sql_where)        
                row = cursor.fetchone()
                if row:
                    if check_password_hash(row[4], _password):
                        session['email'] = row[3]                                               
                        if _remember:
                            resp = make_response(redirect('/'))
                            resp.set_cookie('email', row[3], max_age=COOKIE_TIME_OUT)
                            resp.set_cookie('pwd', _password, max_age=COOKIE_TIME_OUT)
                            resp.set_cookie('rem', 'checked', max_age=COOKIE_TIME_OUT)
                            return resp
                        return redirect('/')
                    else:
                        flash('Invalid Password!')
                        return redirect('/login')
                else:
                    flash('Invalid Email Or Password!')
                    return redirect('/login')
            else:
                flash('Invalid Email Or Password!')
                return redirect('/login')


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
