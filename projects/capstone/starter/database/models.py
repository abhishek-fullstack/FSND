import os
from sqlalchemy import Column, String, Integer, Date, Float, create_engine
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    '''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable
    to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


movies_actors = db.Table(
    'movies_actors',
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movie.id'),
        primary_key=True),
    db.Column(
        'actor_id',
        db.Integer,
        db.ForeignKey('actor.id'),
        primary_key=True))


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    genre = Column(String)
    language = Column(String)
    year = Column(Integer)
    imdb_rating = Column(Float)
    actors = db.relationship('Actor', secondary=movies_actors,
                             backref=db.backref('movies', lazy=True))

    def __init__(self, name, genre, language, year, imdb_rating):
        self.name = name
        self.genre = genre
        self.language = language
        self.year = year
        self.imdb_rating = imdb_rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year
        }

    def detail(self):
        return {
            'id': self.id,
            'name': self.name,
            'genre': self.genre,
            'language': self.language,
            'year': self.year,
            'imdb_rating': self.imdb_rating,
            'no_of_actors': [len(self.actors)],
            'actors': [actor.short() for actor in self.actors]
        }


class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nationality = Column(String)
    date_of_birth = Column(Date)

    def __init__(self, name, nationality, date_of_birth):
        self.name = name
        self.nationality = nationality
        self.date_of_birth = date_of_birth

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def detail(self):
        return {
            'id': self.id,
            'name': self.name,
            'nationality': self.nationality,
            'date_of_birth': self.date_of_birth,
            'no_of_movies': [len(self.movies)],
            'movies': [movie.short() for movie in self.movies]
        }
