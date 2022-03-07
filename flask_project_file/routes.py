from flask import render_template, url_for, flash, redirect
from flask_project_file import app, db, bcrypt
from flask_project_file.forms import RegistrationForm, LoginForm
from flask_project_file.models import User, Post
from flask_login import login_user


posts = [

	{
		'author': 'Billy Bob',
		'title' : '1st Blog Post',
		'content' : 'First post content',
		'date_posted': 'April 20, 2022'
	}
	,
	{
		'author': 'Jane Austen',
		'title' : '2nd Blog Post',
		'content' : 'Second post content',
		'date_posted': 'April 21, 2022'
	}



]


@app.route("/")
@app.route("/home")
def home():
	return render_template('Home.html', posts = posts)

@app.route("/about")
def about():
	return render_template('About.html', title = 'About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created {form.username.data}! You are now able to log in.', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title = 'Log In', form = form)
