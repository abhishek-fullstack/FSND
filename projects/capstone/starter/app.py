import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import setup_db, db_drop_and_create_all, Movie, Actor
from auth.auth import AuthError, requires_auth
import sys


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    Setting up CORS. Allowing '*' for origins.
    '''
    CORS(app, resources={r"/": {"origins": "*"}})

    '''
    Using the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # db_drop_and_create_all()

    '''
    This is just for health check
    Requires no permission
    '''
    @app.route('/')
    def get_greeting():
        return "Hello"
    '''
    This is a helper method to provide custom url to login
    for users and generate reusable token
    '''
    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        auth0_domain = os.environ['AUTH0_DOMAIN']
        api_audience = os.environ['AUTH0_API_AUDIENCE']
        client_id = os.environ['AUTH0_CLIENT_ID']
        callback_url = os.environ['AUTH0_CALLBACK_URL']
        url = f'https://{auth0_domain}/authorize' \
            f'?audience={api_audience}' \
            f'&response_type=token&client_id=' \
            f'{client_id}&redirect_uri=' \
            f'{callback_url}'
        return jsonify({
            'url': url
        })

    '''
    Fetche list of actors
    Can be invoked with view:actor permission
    '''
    @app.route('/actors')
    @requires_auth('view:actor')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({'success': 'True',
                        'total_actors': len(actors),
                        'actors':
                        [actor.short() for actor in actors]})

    '''
    Fetches details of actor with the specified id in the URL
    Can be invoked with view:actor permission
    '''
    @app.route('/actors/<int:actor_id>')
    @requires_auth('view:actor')
    def get_actor_detail(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        else:
            return jsonify({'success': 'True',
                            'actor': actor.detail()})

    '''
    Deletes the actor with the specified id in the URL
    Can be invoked with delete:actor permission
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        else:
            try:
                actor.delete()
                return jsonify({'success': 'True',
                                'deleted_actor': actor.short()})
            except Exception as e:
                abort(422)

    '''
    Creates a new actor with the passed parameters
    Can be invoked with create:actor permission
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actor')
    def create_actor(payload):
        data = request.get_json()
        name = data.get('name')
        nationality = data.get('nationality')
        date_of_birth = data.get('date_of_birth')
        movies = data.get('movies')
        if name is None:
            abort(422)
        try:
            actor = Actor(name=name,
                          nationality=nationality,
                          date_of_birth=date_of_birth)

            if movies is not None:
                movie_list = Movie.query.filter(
                    Movie.id.in_(movies)).all()
                if len(movies) == len(movie_list):
                    actor.movies = movie_list
                else:
                    abort(422)

            actor.insert()
            return jsonify({'success': 'True',
                            'created_actor': actor.short()
                            })
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    '''
    Updates the actor with the specified id in the URL with passed parameters
    Can be invoked with modify:actor permission
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('modify:actor')
    def update_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        else:
            data = request.get_json()
            name = data.get('name')
            nationality = data.get('nationality')
            date_of_birth = data.get('date_of_birth')
            movies = data.get('movies')
            if name is not None:
                actor.name = name
            if nationality is not None:
                actor.nationality = nationality
            if date_of_birth is not None:
                actor.date_of_birth = date_of_birth
            if movies is not None:
                movie_list = Movie.query.filter(
                    Movie.id.in_(movies)).all()
                if len(movies) == len(movie_list):
                    actor.movies = movie_list
                else:
                    abort(422)
            try:
                actor.update()
                return jsonify({'success': 'True',
                                'updated_actor': actor.short()
                                })
            except Exception as e:
                print(sys.exc_info())
                abort(422)

    '''
    Fetche list of movies
    Can be invoked with view:movie permission
    '''
    @app.route('/movies')
    @requires_auth('view:movie')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({'success': 'True',
                        'total_movies': len(movies),
                        'movies':
                        [movie.short() for movie in movies]})

    '''
    Fetches details of movie with the specified id in the URL
    Can be invoked with view:movie permission
    '''
    @app.route('/movies/<int:movie_id>')
    @requires_auth('view:movie')
    def get_movie_detail(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            return jsonify({'success': 'True',
                            'movie': movie.detail()})

    '''
    Deletes the movie with the specified id in the URL
    Can be invoked with delete:movie permission
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            try:
                movie.delete()
                return jsonify({'success': 'True',
                                'deleted_movie': movie.short()})
            except Exception as e:
                abort(422)

    '''
    Creates a new movie with the passed parameters
    Can be invoked with create:movie permission
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie(payload):
        data = request.get_json()
        name = data.get('name')
        genre = data.get('genre')
        language = data.get('language')
        year = data.get('year')
        imdb_rating = data.get('imdb_rating')
        actors = data.get('actors')
        if name is None:
            abort(422)
        try:
            movie = Movie(
                name=name,
                genre=genre,
                language=language,
                year=year,
                imdb_rating=imdb_rating)

            if actors is not None:
                actor_list = Actor.query.filter(
                    Actor.id.in_(actors)).all()
                if len(actors) == len(actor_list):
                    movie.actors = actor_list
                else:
                    abort(422)

            movie.insert()
            return jsonify({'success': 'True',
                            'created_movie': movie.short()
                            })
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    '''
    Updates the movie with the specified id in the URL with passed parameters
    Can be invoked with modify:movie permission
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('modify:movie')
    def update_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            data = request.get_json()
            name = data.get('name')
            genre = data.get('genre')
            language = data.get('language')
            year = data.get('year')
            imdb_rating = data.get('imdb_rating')
            actors = data.get('actors')
            if name is not None:
                movie.name = name
            if genre is not None:
                movie.genre = genre
            if language is not None:
                movie.language = language
            if year is not None:
                movie.year = year
            if imdb_rating is not None:
                movie.imdb_rating = imdb_rating
            if actors is not None:
                actor_list = Actor.query.filter(
                    Actor.id.in_(actors)).all()
                if len(actors) == len(actor_list):
                    movie.actors = actor_list
                else:
                    abort(422)
            try:
                movie.update()
                return jsonify({'success': 'True',
                                'updated_movie': movie.short()
                                })
            except Exception as e:
                print(sys.exc_info())
                abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': 'False',
                        'error': 400,
                        'message': "bad request"
                        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': 'False',
                        'error': 404,
                        'message': "resource not found"
                        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': 'False',
                        'error': 422,
                        'message': "unprocessable"
                        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'success': 'False',
                        'error': 405,
                        'message': "method is not allowed"
                        }), 405

    @app.errorhandler(500)
    def method_not_allowed(error):
        return jsonify({'success': 'False',
                        'error': 500,
                        'message': "internal server error"
                        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
