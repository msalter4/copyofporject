from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from imdb import IMDb
import bcrypt
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='sensitive_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# main variable was undefined, so I defined it with a blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html").replace()
   
@main.route('/signup')
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        email_address = request.form['email_address']

        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, hashed, email_address))

                conn.commit()
                print("Record inserted successfully")
        finally:
            conn.close()
        return redirect(url_for('login')) 
    return render_template('signup.html')

@main.route('/signin')
def signin():
    """if 'quiz_taken' in users_db[username] and users_db[username]['quiz_taken']:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('quiz'))"""
    return render_template('signin.html')

@main.route('/profile') #just your recommendations
def profile():
    if not session.get('user', None):
        return render_template('profile.html')
    
@main.route('/home') #feed
def home():
    return render_template('home.html')

@main.route('/quiz') 
def quiz():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('quiz.html')
