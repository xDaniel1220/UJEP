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


# Functions
def initiateNeo():
        # Delete entire neo4j db
        graph.run('MATCH (n) DETACH DELETE n')

        # Reintiate db
        sol = Node('System', name='Sol')
        cheyenne = Node('System', name='Cheyenne')
        volii = Node('System', name='Volii')
        porrima = Node('System', name='Porrima')
        wolf = Node('System', name='Wolf')
        bessel = Node('System', name='Bessel')
        altair = Node('System', name='Altair')
        alpha_centauri = Node('System', name='Alpha Centauri')

        systems = [sol, cheyenne, volii, porrima, wolf, bessel, altair, alpha_centauri]

        earth = Node('Planet', name='Earth')
        mars = Node('Planet', name='Mars')
        montara = Node('Planet', name='Montana')
        volii_alpha = Node('Planet', name='Volii Alpha')
        porrima2 = Node('Planet', name='Porrima II')
        porrima3 = Node('Planet', name='Porrima III')
        chthonia = Node('Planet', name='Chthonia')
        bessel2 = Node('Planet', name='Bessel II')
        altair2 = Node('Planet', name='Altair II')
        jemison = Node('Planet', name='Jemison')
        akila = Node('Planet', name='Akila')
        gagarin = Node('Planet', name='Gagarin')
        olivas = Node('Planet', name='Olivas')
        planets = [earth, mars, montara, volii_alpha, porrima2, porrima3, chthonia, bessel2, altair2, jemison, akila, gagarin, olivas]

        sol_earth = Relationship(sol, 'HAS_PLANET', earth)
        sol_mars = Relationship(sol, 'HAS_PLANET', mars)
        cheyenne_montara = Relationship(cheyenne, 'HAS_PLANET', montara)
        cheyenne_akila = Relationship(cheyenne, 'HAS_PLANET', akila)
        volii_volii_alpha = Relationship(volii, 'HAS_PLANET', volii_alpha)
        porrima_porrima2 = Relationship(porrima, 'HAS_PLANET', porrima2)
        porrima_porrima3 = Relationship(porrima, 'HAS_PLANET', porrima3)
        wolf_chthonia = Relationship(wolf, 'HAS_PLANET', chthonia) 
        bessel_bessel2 = Relationship(bessel, 'HAS_PLANET', bessel2)
        altair_altair2 = Relationship(altair, 'HAS_PLANET', altair2)
        alpha_centauri_jemison = Relationship(alpha_centauri, 'HAS_PLANET', jemison)
        alpha_centauri_gagarin = Relationship(alpha_centauri, 'HAS_PLANET', gagarin)
        alpha_centauri_olivas = Relationship(olivas, 'HAS_PLANET', jemison)
        relationships = [sol_earth, sol_mars, cheyenne_montara, cheyenne_akila, volii_volii_alpha,
                         porrima_porrima2, porrima_porrima3, wolf_chthonia, bessel_bessel2, altair_altair2,
                         alpha_centauri_jemison, alpha_centauri_gagarin, alpha_centauri_olivas]

        for system in systems:
            graph.create(system)

        for planet in planets:
            graph.create(planet)

        for relationship in relationships:
            graph.create(relationship)


initiateNeo()


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
        user_settings_json = dumps(user_settings.find_one({'username': user}))

        if user_settings_json != 'null':
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
        print('We get data from Redis')
        print(data)
        return data
    else:
        user_json = dumps(users.find_one({'username': user}))

        if user_json != 'null':
            redis.set(user, user_json)
            redis.expire(user, redis_cache_time)

        if user_json == 'null':
            session.clear()
            # return redirect(url_for('login'))

        print('We get data from MongoDB')
        return json.loads(user_json)


# Routes
@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404


@app.route('/')
@app.route('/home')
def index():
    if session.get('username') is not None:
        get_user(session['username'])
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        found_user = get_user(username)

        if found_user is not None:
            print(get_user(username))
            return render_template('register.html', error='User already exists')

        encrypted_password = encrypt_password(password)
        users.insert_one({"username": username, "password": encrypted_password})

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        dob = request.form['dob']
        email = request.form['email']

        json_file = {'username': username, 'first_name': first_name, 'last_name': last_name, 'address': address, 'dob': dob, 'email': email}
        user_settings.insert_one(json_file)

        session['username'] = request.form['username']
        session['password'] = request.form['password']
        print(username)
        print(encrypted_password)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if get_user(username) is None:
            return render_template('login.html', error='Invalid user')

        found_user = get_user(username)
        if found_user and check_password(password, found_user['password']):
            session['username'] = found_user['username']
            session['password'] = found_user['password']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid password')
        
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