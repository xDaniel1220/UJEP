from flask import Flask, render_template, url_for, request, redirect, session
from redis import Redis
from pymongo import MongoClient

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
mongo = MongoClient("mongodb://mongodb:27017", connect=False)

@app.route('/')
def index():
    if 'username' in session:
        return 'Get out of here ' + session['username']
    
    return render_template('index.html', slur = 'a charm')

@app.route('/redis')
def redis_route():
    redis.incr('hits')
    counter = str(redis.get('hits'), 'utf-8')
    return "This web page has been viewed " + counter + " time(s)"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        mongo.db.users.insert_one({"name":"Daniel Blaha"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)