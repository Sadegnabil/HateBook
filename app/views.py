from flask import render_template, flash, redirect, url_for, send_from_directory, session, request, g
from app import app, models, db
from .forms import *
import datetime
import os
import hashlib

# Create the route for the index
@app.route('/', methods=['GET', 'POST'])
def index():
	login_form = Login()
	register_form = Register()

	print "*******************************"
	print login_form.validate_on_submit()
	print register_form.validate_on_submit()
	print login_form.username_login.data
	print register_form.username_register.data
	row = models.Users.query.filter_by(username = "Nabil").first()
	print row.password
	print "*******************************"


	if login_form.validate_on_submit():
		user = models.Users.query.filter_by(username = login_form.username_login.data).first()
		password = hashlib.sha1(login_form.password_login.data).hexdigest()
		if password == user.password:
			session['user'] = user.username
			return redirect(url_for('profile'))

	elif register_form.validate_on_submit():
		db.session.add(models.Users(username = register_form.username_register.data, password = hashlib.sha1(register_form.password_register.data).hexdigest()))
		db.session.commit()
		session['user'] = register_form.username_register.data
		return redirect(url_for('profile'))

	login_form.username_login.data = ""
	login_form.password_login.data = ""

	register_form.username_register.data = ""
	register_form.password_register.data = ""


	# return request.form['btn']
		# if request.form['btn'] == 'login':

		# 	if request.method == 'POST':
		# 		session.pop('user', None)

		# 		if request.form['password'] == 'password':
		# 			session['user'] = request.form['username']
		# 			return redirect(url_for('profile'))

		# elif request.form['btn'] == 'signin':
		# 	return 'LOL'

	return render_template('index.html', login_form = login_form, register_form = register_form)

@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']
	return 'Nope'

@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return redirect(url_for('index'))

@app.route('/profile')
def profile():
	print g.user != None
	print g.user
	print models.Users.query.filter_by(username = g.user).first()
	if g.user:
		return render_template('profile.html', user = models.Users.query.filter_by(username = g.user).first())

	return redirect(url_for('index'))

@app.before_request
def before_request():
	g.user=None
	if 'user' in session:
		g.user = session['user']