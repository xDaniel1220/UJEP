from flask import Flask, render_template, url_for, request, redirect, session
from redis import Redis
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

redis = Redis(host='redis', port=6379)
mongo = MongoClient("mongodb://localhost:27017", connect=False)

db = mongo['NSQL']
users = db['Users']

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def get_password(self):
        return self.password
    
    def get_username(self):
        return self.username


def check_password(password, encrypted):
    return bcrypt.checkpw(password.encode('utf-8'), encrypted.encode('utf-8'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        users.insert_one({"username" : new_user.get_username(), "password" : new_user.get_password()})
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        found_user = users.find_one({"username" : username})

        if found_user and check_password(password, found_user['password']):
            session['username'] = found_user['username']
            session['password'] = found_user['password']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid user')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if session.get('username') is not None:
        found_user = users.find_one({"username" : session['username']})
        return render_template('dashboard.html', user=found_user)
    else:
        return redirect(url_for('login'))

@app.route('/allusers')
def allusers():
    return render_template('users.html', users=users.find())

@app.route('/edit/<user>')
def edit(user):
    found_user = users.find_one({"username" : user})
    return 'Hello ' + found_user['username'] + '</br> Your password is ' + found_user['password']

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)