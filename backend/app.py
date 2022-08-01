import os
import redis
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, session, escape
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
#app.secret_key = os.environ.get('SECRET_KEY', default=None)
app.secret_key = '1234'

coherence_dev=os.environ.get('COHERENCE_DEV')
dbname=os.environ['DB_NAME']
dbuser=os.environ['DB_USER']
dbpass=os.environ['DB_PASSWORD']

dbsocket=""
dbendpoint=""
dbhost=""
dbport=""
redishost=""
redisport=""
for env in os.environ:
    if env.endswith("DB1_SOCKET"):
        dbsocket=os.environ[env]
    if env.endswith("DB1_ENDPOINT"):
        dbendpoint=os.environ[env]
    if env == "DB_HOST":
        dbhost=os.environ[env]
    if env.endswith("DB1_PORT"):
        dbport=os.environ[env]
    if env.endswith("REDIS_IP"):
        redishost=os.environ[env]
    if env.endswith("REDIS_PORT"):
        redisport=os.environ[env]

print ("DBSOCKET: %s" % (dbsocket))
print ("DBENDPOINT: %s" % (dbendpoint))
print ("DBHOST: %s" % (dbhost))
print ("DBPORT: %s" % (dbport))
print ("REDISHOST: %s" % (redishost))
print ("REDISPORT: %s" % (redisport))

#REDIS_URL = os.environ.get('REDIS_URL')
redis_url = f"redis://{redishost}:{redisport}"

store = redis.Redis.from_url(redis_url)

if coherence_dev is not None and coherence_dev == "true":
    if dbhost is not None and dbhost != "":
        url = f"postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}"
    else:
        url = f"postgresql://{dbuser}:{dbpass}@localhost:{dbport}/{dbname}"
else:
    if dbendpoint != "":
        url = f"postgresql://{dbuser}:{dbpass}@{dbendpoint}:{dbport}/{dbname}"
    else:
        url = f"postgresql://{dbuser}:{dbpass}@/{dbname}?host={dbsocket}"

print ("URI: %s" % (url))
#app.config['SQLALCHEMY_DATABASE_URI'] = url
#
#
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
#
#from models import Message
#db.create_all()
#db.session.commit()


@app.route('/')
def index():
    if 'username' in session:
        username = escape(session['username'])
        visits = store.hincrby(username, 'visits', 1)
        store.expire(username, 120)

        return '''
            Logged in as {0}.<br>
            Visits: {1}
            '''.format(username, visits)

    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        session['username'] = request.form['username']
        return redirect('/')

    return '''
        <form method="post">
        <p><input type=text name=username>
        <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():

    session.pop('username', None)
    return redirect('/')
