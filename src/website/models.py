# create database models
# the . means you can import from the current package
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
    
# EVERY TABLE NEEDS A PRIMARY KEY!!!!

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), unique=True)
    watched_movies = db.relationship('WatchedMovie')
    reviews = db.relationship('Review')
    recommendations = db.relationship('Recommendation', backref='user')
    friends = db.relationship('Friend', foreign_keys='Friend.user_id_1')

class Movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    url = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer)
    genres = db.relationship('Genre')
    languages = db.relationship('Language')
    directors = db.relationship('Director')
    writers = db.relationship('Writer')
    actors = db.relationship('Actor')

    def __init__(self, movie_id, title, url, year):
        self.movie_id = movie_id
        self.title = title
        self.url = url
        self.year = year
        

# a movie_id will have multiple relationships and one of them is a relationship with a table names genre
# which will have multiple genres.
class Genre(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    genre = db.Column(db.String(25))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, movie_id, genre):
        self.movie_id = movie_id
        self.genre = genre

class Language(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    language = db.Column(db.String(25))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, movie_id, language):
        self.movie_id = movie_id
        self.language = language

class Director(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    director = db.Column(db.String(25))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, movie_id, director):
        self.movie_id = movie_id
        self.director = director

class Writer(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    writer = db.Column(db.String(25))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, movie_id, writer):
        self.movie_id = movie_id
        self.writer = writer

class Actor(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    actor = db.Column(db.String(25))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, movie_id, actor):
        self.movie_id = movie_id
        self.actor = actor

class WatchedMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    timestamp = db.Column(db.DateTime(timezone=True), default =func.now())

    def __init__(self, user_id, movie_id):
        self.user_id = user_id
        self.movie_id = movie_id

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    timestamp = db.Column(db.DateTime(timezone=True), default =func.now())
    review_text = db.Column(db.Text)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))

    # a better way of having 10 recommendations rather than individually listing each rec column
    __table_args = (
        db.CheckConstraint("user_id <= 10"),
    )

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id_2 = db.Column(db.Integer)
