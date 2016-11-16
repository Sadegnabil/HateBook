from flask import render_template, redirect, url_for, session, request
from app import app, models, db
from .forms import *
import datetime
import os
import hashlib 		# For the password
from shutil import copyfile 	# To copy the default profile picture
from werkzeug.utils import secure_filename	# To upload the images


# Set the allowed extensions for pictures
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Set the maximum number of reports
MAX_REPORTS = 1

# Create the route for the index
@app.route('/', methods=['GET', 'POST'])
def index():

	# Initialise the forms
	login_form = Login()
	register_form = Register()

	# Initialise the error lists
	errorLogin = []
	errorRegister = []

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

				# If the password is wrong
				else:
					# Open the log file and print the error
					with open('app/static/logs.txt', 'w') as file:
						timeLog = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
						errorLog = "[" + timeLog + "] Login attempted fail: Wrong password. User: " + user.username
						file.write(errorLog)

			
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
					birth = register_form.birth_register.data))
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
		register_form.birth_register.data = ""

	# Render the index
	return render_template('index.html', login_form = login_form, register_form = register_form, errorLogin=errorLogin, errorRegister = errorRegister)




# Create a rout for the profile page
@app.route('/profile/<usernamePage>', methods=['GET', 'POST'])
def profile(usernamePage):

	# If there is a user connected display the profile page
	if 'user' in session:

		picture_errors = []

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

				# Commit the changes
				db.session.commit()


			# If the user is changing the profile picture
			else:
				file = request.files['file']
				if file:
					filename = secure_filename(file.filename)
					extension = filename.rsplit('.', 1)[1]
					# Check the picture format
					if extension in ALLOWED_EXTENSIONS:
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], currentUser.username + ".jpg"))
					else:
						picture_errors.append("Wrong format ! Please upload a picture in .png, .jpg or .jpeg")

		# Retrieve the userPage
		userPage = db.session.query(models.Users).filter_by(username = usernamePage).first()

		# Return the profile page
		return render_template('profile.html', profile = profile_form,
			currentUser = currentUser,
			userPage = userPage,			
			timeNow = datetime.datetime.utcnow(), picture_errors=picture_errors)

	# Otherwise redirect the user to the index
	return redirect(url_for('index'))




# Create a route for the newsfeed page
@app.route('/newsfeed', methods=['GET', 'POST'])
def newsfeed():

	# If there is a user connected display the profile page
	if 'user' in session:

		# Create the forms
		postForm = Post()
		# commentForm = Comment()

		# Query the user from the database
		user = db.session.query(models.Users).filter_by(username = session['user']).first()

		if request.method == 'POST':
			if postForm.validate_on_submit():
				newPost = models.Posts(date = datetime.datetime.utcnow(), text = postForm.text_post.data, author = user)
				db.session.add(newPost)
				db.session.commit()
				postForm.text_post.data = ""


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




# Route used to add a comment
@app.route('/addComment/<id>/<text>')
def addComment(id, text):
	
	# Retrieve the post
	post = db.session.query(models.Posts).get(int(id))
	# Increment the number of comments in this post
	post.comments_number += 1

	# Create a new comment
	newComment = models.Comments(date = datetime.datetime.utcnow(), text = text, 
		author = db.session.query(models.Users).filter_by(username = session['user']).first(), 
		post = post)

	# Add the comment to the database and commit the changes
	db.session.add(newComment)
	db.session.commit()

	# Return the newsfeed page
	return redirect(url_for('newsfeed'))




# Route used if the comment is empty
@app.route('/addComment/<id>/')
def emptyComment(id):
	# Just return newsfeed
	return redirect(url_for('newsfeed'))




# Route used to add a report
@app.route('/report/<type>/<id>')
def report(type, id):

	# Retrive the user
	user = db.session.query(models.Users).filter_by(username = session['user']).first()

	# If it's a post
	if type == 'post':

		# Retrieve the post
		post = db.session.query(models.Posts).get(int(id))

		# Go through the report associated to this post 
		for report in post.reports:
			# If the user has already created a report about this post just return newsfeed 
			# One user can report a post at most once
			if report.author.username == session['user']:
				return redirect(url_for('newsfeed'))

		# If the user hasn't reported the post create a new report and add it to the database
		newReport = models.Reports(author=user, post=post)
		db.session.add(newReport)

		# Increment the number of reports
		post.reports_number += 1
		db.session.commit()

		# If the post has been reported by too many people delete it
		if post.reports_number == MAX_REPORTS:
			deleteElement(post)


	# If it's a comment
	elif type == 'comment':

		# Retrieve the comment
		comment = db.session.query(models.Comments).get(int(id))

		# Check if the user has already reported the comment
		for report in comment.reports:
			# If the user has already created a report about this comment just return newsfeed 
			# One user can report a comment at most once
			if report.author.username == session['user']:
				return redirect(url_for('newsfeed'))

		# If the user hasn't already reported the comment create a new report and add it to the database
		newReport = models.Reports(author=user, comment=comment)
		db.session.add(newReport)

		# Increment the number of reports
		comment.reports_number += 1
		db.session.commit()

		# If the comment has too many reports delete it
		if comment.reports_number == MAX_REPORTS:
			deleteElement(comment)

			# Decrease the number of comments
			post = db.session.query(models.Posts).get(int(comment.post_id))
			post.comments_number -= 1

			# Commit the changes
			db.session.commit()


	# Return newsfeed
	return redirect(url_for('newsfeed'))




# Function used to delete a comment or a post
def deleteElement(element):

	# Delete all the reports about the element
	for report in element.reports:
		db.session.delete(report)

	# Delete the element
	db.session.delete(element)
	# Commit the changes
	db.session.commit()

	# Return newsfeed
	return redirect(url_for('newsfeed'))




# Function used to handle 'hates'
@app.route('/toogleHate/<id>')
def toogleHate(id):

	# Retrieve the post
	post = db.session.query(models.Posts).get(int(id))
	# Retrive the user
	user = db.session.query(models.Users).filter_by(username = session['user']).first()

	# If the user has already 'hated' the post, delete the hate and decrease the hate number
	for hate in post.hates:
		if hate.author.username == session['user']:
			db.session.delete(hate)
			post.hates_number -= 1

			# Commit the changes and return newsfeed
			db.session.commit()
			return redirect(url_for('newsfeed'))

	# If the user hasn't already hated the post, create the new hate and add it to the database
	newHate = models.Hates(author = user, post = post)
	db.session.add(newHate)

	# Increase the number of hates and commit the changes
	post.hates_number += 1
	db.session.commit()

	# Return newsfeed
	return redirect(url_for('newsfeed'))