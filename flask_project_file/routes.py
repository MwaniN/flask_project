import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from matplotlib.pyplot import title
from flask_project_file import app, db, bcrypt
from flask_project_file.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_project_file.models import User, Music
from flask_login import login_user, current_user, logout_user, login_required


posts = [

	{
		'author': 'Pied Piper',
		'title' : 'Welcome!',
		'content' : 'First log in, then you can access the music page.',
		'date_posted': 'May 01, 2022'
	}



]


@app.route("/")
@app.route("/home")
def home():
	logged_in = False
	if current_user.is_authenticated:
		logged_in = True

	return render_template('Home.html', logged_in=logged_in)

@app.route("/about")
def about():
	return render_template('About.html', title = 'About')

@app.route("/music", methods=['GET'])
@login_required
def music():
	songs = [item[0] for item in Music.query.with_entities(Music.title)]
	artist_name = [item[0] for item in Music.query.with_entities(Music.artist_name)]
	path_to_mp3 = [item[0] for item in Music.query.with_entities(Music.path_to_mp3)]
	image_url = [item[0] for item in Music.query.with_entities(Music.image_url)]
	mp3_file = [item[0] for item in Music.query.with_entities(Music.mp3_file)]

	#songs = os.listdir('flask_project_file/static/music/')
	return render_template('Music.html', music_table=zip(image_url,songs,artist_name,path_to_mp3))

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
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
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('music'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title = 'Log In', form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)


	i.save(picture_path)
	return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title = 'Account', image_file=image_file, form=form)