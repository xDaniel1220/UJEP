from flask import Flask, render_template, url_for, request, redirect, session
from redis import Redis
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

redis = Redis(host='redis', port=6379)
mongo = MongoClient("mongodb://mongodb:27017", connect=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = user.username
            session['password'] = user.password
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Inavlid user')
        
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if session['username']:
        user = User.query.filter_by(username=session['username']).first()
        return render_template('dashboard.html', user=user)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)