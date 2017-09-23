# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import requests
import json


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


@app.route('/')
def welcome():
    if not session.get('logged_in'):
	   return redirect(url_for('login'))
    else:
        return redirect(url_for('show_routes'))


@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute('insert into entries (title, text) values (?, ?)',
		[request.form['title'], request.form['text']])
	db.commit()
	flash('New entry was succesfully posted')
	return redirect(url_for('show_entries'))


@app.route('/route')
def show_routes():
	return render_template('show_routes.html')


@app.route('/route/add', methods=['POST'])
def add_route():
	if not session.get('logged_in'):
		abort(401)
	print request.form['title']
	return redirect(url_for('show_routes'))

#simulate QR code
@app.route('/qrcode')
def show_qrcode():
    cur_location = get_location()
    print cur_location
    return render_template('qrcode.html')

#helper function to get current geolocation

def get_location():
    r = requests.get('http://freegeoip.net/json')
    j = json.loads(r.text)
    return [j['latitude'], j['longitude']]


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_routes'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))




































