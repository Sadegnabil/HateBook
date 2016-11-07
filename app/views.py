from flask import render_template, flash, redirect, url_for, send_from_directory, session, request, g
from app import app, models, db
from .createTask import CreateTask
import datetime
import os

# Create the route for the index
@app.route('/', methods=['GET', 'POST'])
def index():
	if form.validate_on_submit():
	# return request.form['btn']
		if request.form['btn'] == 'login':

			if request.method == 'POST':
				session.pop('user', None)

				if request.form['password'] == 'password':
					session['user'] = request.form['username']
					return redirect(url_for('profile'))

		elif request.form['btn'] == 'signin':
			return 'LOL'

	return render_template('index.html')

@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']
	return 'Nope'

@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return 'Dropped'

@app.route('/profile')
def profile():
	if g.user:
		return render_template('profile.html', name=session['user'])

	return redirect(url_for('index'))

@app.before_request
def before_request():
	g.user=None
	if 'user' in session:
		g.user = session['user']