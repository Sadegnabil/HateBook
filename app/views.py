from flask import render_template, flash, redirect, url_for, send_from_directory, session, request, g
from app import app, models, db
from .forms import *
import datetime
import os
import hashlib

# Create the route for the index
@app.route('/', methods=['GET', 'POST'])
def index():

	# Initialise the forms
	login_form = Login()
	register_form = Register()

	# If the login_form is validated
	if login_form.validate_on_submit():
		# Retrieve the user
		user = models.Users.query.filter_by(username = login_form.username_login.data).first()
		# If the user exists
		if user != None:
			# Encrypt the password
			password = hashlib.sha1(login_form.password_login.data).hexdigest()
			# If the password is correct
			if password == user.password:
				# Save the username
				session['user'] = user.username

				return redirect(url_for('profile'))

	# If the register_form is validated
	elif register_form.validate_on_submit():
		# Create the user
		db.session.add(models.Users(username = register_form.username_register.data,
			password = hashlib.sha1(register_form.password_register.data).hexdigest(), registration_date = datetime.datetime.utcnow().strftime("%B %d, %Y")))
		db.session.commit()
		# Save the username
		session['user'] = register_form.username_register.data
		# Redirect to the profile page
		return redirect(url_for('profile'))

	# Reset the forms fields
	login_form.username_login.data = ""
	login_form.password_login.data = ""
	register_form.username_register.data = ""
	register_form.password_register.data = ""

	# Render the index
	return render_template('index.html', login_form = login_form, register_form = register_form)



# @app.route('/getsession')
# def getsession():
# 	if 'user' in session:
# 		return session['user']
# 	return 'Nope'



@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return redirect(url_for('index'))



@app.route('/profile', methods=['GET', 'POST'])
def profile():

	if g.user:

		user = db.session.query(models.Users).filter_by(username = g.user).first()
		db.session.query(models.Users).filter_by(username = g.user).first().name = "abc"

		profile_form = Profile()

		print user
		user.name = profile_form.name.data
		db.session.commit()

		return render_template('profile.html', user = user, profile = profile_form)

	return redirect(url_for('index'))



@app.before_request
def before_request():
	g.user=None
	if 'user' in session:
		g.user = session['user']