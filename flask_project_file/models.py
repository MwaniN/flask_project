from flask_project_file import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default ='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

class Music(db.Model):
	title = db.Column(db.String(100), nullable=False)
	artist_name = db.Column(db.String(100), nullable=False)
	song_id = db.Column(db.String(40), primary_key=True)
	duration = db.Column(db.String(10), nullable=False)
	popularity = db.Column(db.Integer, nullable=False)
	explicit = db.Column(db.Integer, nullable=False)
	album_id = db.Column(db.String(100), nullable=False)
	release_date = db.Column(db.String(10), nullable=False)
	album_name = db.Column(db.String(100), nullable=False)
	artist_id = db.Column(db.String(100), nullable=False)
	mp3_file = db.Column(db.String(100), nullable=False)
	path_to_mp3 = db.Column(db.String(100), nullable=False)
	image_url = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"Music('{self.title}', '{self.artist_name}', '{self.path_to_mp3}', '{self.image_url}', '{self.mp3_file})"
