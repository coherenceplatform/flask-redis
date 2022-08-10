import os
import redis
from flask import Flask, render_template, request, url_for, redirect, session, escape

app = Flask(__name__)
app.secret_key = '1234'

coherence_dev=os.environ.get('COHERENCE_DEV')
port=os.environ.get('PORT')

redishost=""
redisport=""
for env in os.environ:
    if env.endswith("REDIS_IP"):
        redishost=os.environ[env]
    if env.endswith("REDIS_PORT"):
        redisport=os.environ[env]

redis_url = f"redis://{redishost}:{redisport}"

store = redis.Redis.from_url(redis_url)

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
