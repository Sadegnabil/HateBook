from flask import render_template, flash, redirect, url_for, send_from_directory, session, request, g
from app import app, models, db
from .forms import *
import datetime
import os
import hashlib 		# For the password
from shutil import copyfile 	# To copy the default profile picture
from werkzeug.utils import secure_filename	# To upload the images

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Create the route for the index
@app.route('/', methods=['GET', 'POST'])
def index():

	# Initialise the forms
	login_form = Login()
	register_form = Register()

	# Initialise the error lists
	errorLogin = []
	errorRegister = []

	# Initialise the modal variable to 0
	# modal = 0

	if request.method == 'POST':
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

					# Directly redirect on newsfeed
					return redirect(url_for('newsfeed'))
			
			# Append the error
			errorLogin.append("Wrong password or username")
			# Delete the password
			login_form.password_login.data = ""


		# If the register_form is validated
		elif register_form.validate_on_submit():

			# Check if the username is already taken
			if models.Users.query.filter_by(username = register_form.username_register.data).first() != None:
				# Append the error and reset the password field
				errorRegister.append("Username already taken")
				register_form.password_register.data = ""

			else:
				# Encrypt the password
				tmpPassword = hashlib.sha1()
				tmpPassword.update(register_form.password_register.data.encode('utf-8'))

				# Create the user
				db.session.add(models.Users(username = register_form.username_register.data,
					password = tmpPassword.hexdigest(), 
					registration_date = datetime.datetime.utcnow(),
					name = register_form.name_register.data, surname = register_form.surname_register.data,
					country = register_form.country_register.data))
				db.session.commit()
				# Save the username
				session['user'] = register_form.username_register.data
				# Create the profile picture
				destination = "app/static/images/profile_pictures/" + register_form.username_register.data + ".jpg"
				copyfile('app/static/images/profile_pictures/default_profile_picture.jpg', destination)
				# Redirect to the profile page
				return redirect('/profile/' + session['user'])

	else:

		# Reset the forms fields
		login_form.username_login.data = ""
		login_form.password_login.data = ""
		register_form.username_register.data = ""
		register_form.password_register.data = ""
		register_form.name_register.data = ""
		register_form.surname_register.data = ""
		register_form.country_register.data = ""

	# Render the index
	return render_template('index.html', login_form = login_form, register_form = register_form, errorLogin=errorLogin, errorRegister = errorRegister)



# Create a rout for the profile page
@app.route('/profile/<usernamePage>', methods=['GET', 'POST'])
def profile(usernamePage):

	# If there is a user connected display the profile page
	if 'user' in session:

		# Query the user from the database
		currentUser = db.session.query(models.Users).filter_by(username = session['user']).first()

		# Create the profile form
		profile_form = Profile()

		# If it's a POST method change the fields
		if request.method == 'POST':

			# If the user is modifying the profile information
			if len(request.form) != 0:
				
				# For each field in the form check if there is a valid entry and update the database
				if profile_form.name_profile.data != "":
					currentUser.name = profile_form.name_profile.data
				if profile_form.surname_profile.data != "":
					currentUser.surname = profile_form.surname_profile.data
				if profile_form.birth_profile.data != "":
					currentUser.birth = profile_form.birth_profile.data
				if profile_form.country_profile.data != "":
					currentUser.country = profile_form.country_profile.data

				# Commit the changes
				db.session.commit()


			# If the user is changing the profile picture
			else:
				file = request.files['file']
				if file:
					filename = secure_filename(file.filename)
					extension = filename.rsplit('.', 1)[1]
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], currentUser.username + ".jpg"))

		# Retrieve the userPage
		userPage = db.session.query(models.Users).filter_by(username = usernamePage).first()

		# Return the profile page
		return render_template('profile.html', profile = profile_form,
			currentUser = currentUser, 
			currentUser_avatar_filename = "images/profile_pictures/" + currentUser.username + ".jpg",
			userPage = userPage,
			userPage_avatar_filename = "images/profile_pictures/" + userPage.username + ".jpg", 			
			timeNow = datetime.datetime.utcnow())

	# Otherwise redirect the user to the index
	return redirect(url_for('index'))




# Create a route for the newsfeed page
@app.route('/newsfeed', methods=['GET', 'POST'])
def newsfeed():

	# If there is a user connected display the profile page
	if 'user' in session:

		# Create the post form
		postForm = Post()

		# Query the user from the database
		user = db.session.query(models.Users).filter_by(username = session['user']).first()

		if request.method == 'POST' and postForm.validate_on_submit():
			newPost = models.Posts(date = datetime.datetime.utcnow(), text = postForm.text.data, author = user)
			db.session.add(newPost)
			db.session.commit()
			postForm.text.data = ""

		# Query the different posts from the database
		posts = models.Posts.query.all()


		# Return the newsfeed page
		return render_template('newsfeed.html', currentUser = user, posts = posts, postForm = postForm,
			currentUser_avatar_filename = "images/profile_pictures/" + user.username + ".jpg", timeNow = datetime.datetime.utcnow())

	# Otherwise redirect the user to the index
	return redirect(url_for('index'))



# Route used to drop the session (disconnect the user)
@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return redirect(url_for('index'))




# Route used to delete an account
@app.route('/deleteaccount')
def deleteaccount():
	# Retrive the user
	user = db.session.query(models.Users).filter_by(username = session['user']).first()
	# Delete the profile picture
	os.remove("app/static/images/profile_pictures/" + user.username + ".jpg", dir_fd=None)
	# Delete the user
	db.session.delete(user)
	db.session.commit()
	# Drop the session
	return redirect(url_for('dropsession'))
