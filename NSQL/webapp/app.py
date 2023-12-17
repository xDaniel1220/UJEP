from flask import Flask, render_template, url_for, request, redirect, session
from redis import Redis
from pymongo import MongoClient
from py2neo import Graph, Node, Relationship
import bcrypt
import json
from bson.json_util import dumps

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# Redis setup
redis = Redis(host='redis', port=6379)
redis_cache_time = 10

# Mongo setup
mongo = MongoClient("mongodb://mongodb:27017", connect=False)
db = mongo['NSQL']
users = db['Users']
user_settings = db['Settings']

# Neo4j setup
graph = Graph('bolt://neo4j:7687', auth=('neo4j', 'adminpass'))

sol = Node('System', name='Sol', spectral_class='G2', temperature=5830, mass=1, radius=696300, magnitude=4.85)
systems = [sol]

earth = Node('Planet', name="Earth", planet_type="Rock", gravity=1, temperature='Cold',
             atmosphere='Low CO2', magnetosphere=None, water='Safe', fauna=0,
             flora=0, organic_resources=0, inorganic_resources=5, biomes=2)
mars = Node('Planet', name="Mars", planet_type="Rock", gravity=1, temperature='Cold',
             atmosphere='Low CO2', magnetosphere=None, water='Safe', fauna=0,
             flora=0, organic_resources=0, inorganic_resources=5, biomes=2)
planets = [earth, mars]

sol_earth = Relationship(sol, 'HAS_PLANET', earth)
sol_mars = Relationship(sol, 'HAS_PLANET', mars)
relationships = [sol_earth, sol_mars]

for system in systems:
    graph.create(system)

for planet in planets:
    graph.create(planet)

for relationship in relationships:
    graph.create(relationship)

# Functions
def check_password(password, encrypted):
    return bcrypt.checkpw(password.encode('utf-8'), encrypted.encode('utf-8'))

def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Get user_settings from Redis. If not in Redis get from MongoDB and store in Redis
def get_user_settings(user):
    if redis.exists(f"{user}_settings"):
        data = json.loads(redis.get(f"{user}_settings").decode('utf-8'))
        return data
    else:
        user_settings_json = dumps(user_settings.find_one({'username' : user}))
        redis.set(f"{user}_settings", user_settings_json)
        redis.expire(f"{user}_settings", redis_cache_time)

        # Checking if user_settings_json is null. If yes change it into a dictionary
        if user_settings_json == 'null':
            user_settings_json = '{}'

        return eval(user_settings_json)
# Get user from Redis. If not in Redis get from MongoDB and store in Redis
def get_user(user):
    if redis.exists(user):
        data = json.loads(redis.get(user).decode('utf-8'))
        return data
    else:
        user_json = dumps(users.find_one({'username' : user}))
        redis.set(user, user_json)
        redis.expire(user, redis_cache_time)
        return eval(user_json)

# Routes
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
        encrypted_password = encrypt_password(password)
        users.insert_one({"username": username, "password": encrypted_password})

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        dob = request.form['dob']
        email = request.form['email']

        json = {'username': username, 'first_name': first_name, 'last_name': last_name, 'address': address, 'dob': dob, 'email': email}
        user_settings.insert_one(json)

        session['username'] = username
        session['password'] = encrypted_password
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        found_user = get_user(username)

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
        found_user = get_user(session['username'])
        return render_template('dashboard.html', user=found_user)
    else:
        return redirect(url_for('login'))

@app.route('/settings/<user>', methods = ['GET', 'POST'])
def edit_user(user):
    if request.method == 'GET':
        edit_user = get_user(user)
        json = get_user_settings(user)
        return render_template('settings.html', user = edit_user, user_settings = json)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        dob = request.form['dob']
        email = request.form['email']

        has_settings = user_settings.find_one({'username' : user})

        json = {'username' : user, 'first_name' : first_name, 'last_name' : last_name, 'address' : address, 'dob' : dob, 'email' : email}

        if has_settings:
            user_settings.update_many({'username' : user}, {'$set' : json})
        else:
            user_settings.insert_one(json)
        
        return redirect(url_for('dashboard'))

@app.route('/database')
def database():
    if session.get('username') is not None:
        found_user = get_user(session['username'])
        return render_template('database.html', user=found_user)
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)