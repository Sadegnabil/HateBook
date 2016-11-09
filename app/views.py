from flask import render_template, flash, redirect, url_for, send_from_directory, session, request, g
from app import app, models, db
from .forms import *
import datetime
import os
import hashlib
from werkzeug.utils import secure_filename
# from PIL import Image
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

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
			tmpPassword = hashlib.sha1()
			tmpPassword.update(login_form.password_login.data.encode('utf-8'))
			password = tmpPassword.hexdigest()
			# If the password is correct
			if password == user.password:
				# Save the username
				session['user'] = user.username

				return redirect(url_for('profile'))

	# If the register_form is validated
	elif register_form.validate_on_submit():
		
		# Encrypt the password
		tmpPassword = hashlib.sha1()
		tmpPassword.update(register_form.password_register.data.encode('utf-8'))

		# Create the user
		db.session.add(models.Users(username = register_form.username_register.data,
			password = tmpPassword.hexdigest(), 
			registration_date = datetime.datetime.utcnow().strftime("%B %d, %Y"),
			name = register_form.name_register.data, surname = register_form.surname_register.data,
			country = register_form.country_register.data))
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
	register_form.name_register.data = ""
	register_form.surname_register.data = ""
	register_form.country_register.data = ""

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

	# If there is a user connected display the profile page
	if g.user:

		# Query the user from the database
		user = db.session.query(models.Users).filter_by(username = g.user).first()

		# Create the profile form
		profile_form = Profile()

		# If it's a POST method change the fields
		if request.method == 'POST':

			# For each field in the form check if there is a valid entry and update the database
			if profile_form.name_profile.data != "":
				user.name = profile_form.name_profile.data
			if profile_form.surname_profile.data != "":
				user.surname = profile_form.surname_profile.data
			if profile_form.birth_profile.data != "":
				user.birth = profile_form.birth_profile.data
			if profile_form.country_profile.data != "":
				user.country = profile_form.country_profile.data

			# Commit the changes
			db.session.commit()
			
			# file = request.files['file']
			# if file:
			# 	filename = secure_filename(file.filename)
			# 	extension = filename.rsplit('.', 1)[1]
			# 	file.save(os.path.join(app.config['UPLOAD_FOLDER'], user.username + ".jpg"))
				
				

		# Return the profile page
		return render_template('profile.html', user = user, profile = profile_form,
			avatar_filename = "images/profile_pictures/" + user.username + ".jpg")

	# Otherwise redirect the user to the index
	return redirect(url_for('index'))


@app.before_request
def before_request():
	g.user=None
	if 'user' in session:
		g.user = session['user']