import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Movie, Actor
import datetime
from auth import requires_auth, AuthError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # enable scripts running on other domains to access app resources
    # allow connections from all origins
    CORS(app, resources={r'*': {'origins': '*'}})
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Authorization, Content-Type')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, DELETE, POST, PATH')

        return response

    @app.route('/')
    def home_screen():
        return """
            Valid Endpoints:
                GET '/actors',
                GET '/movies',
                DELETE '/actors/<int:actor_id>',
                DELETE '/movies/<int:movie_id>',
                POST '/actors',
                POST '/movies',
                PATCH '/actors/<int:actor_id>',
                PATCH '/movies/<int:movie_id>'
            """

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies():
       # get all movies and format
        try:
            movies = Movie.query.all()
            movies = [movie.format() for movie in movies]

            return jsonify({
                "success": True,
                "movies": movies
            })
        except Exception:
            abort(404)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors():
        # get all actors and format
        try:
            actors = Actor.query.all()
            actors = [actor.format() for actor in actors]

            return jsonify({
                "success": True,
                "actors": actors
            })
        except Exception:
            abort(404)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        # get actor details and delete if found, else abort
        actor = Actor.query.get(actor_id)
        if actor:
            actor.delete()

            return jsonify({
                "success": True,
                "deleted_actor_id": actor_id
            })
        abort(404)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        # get movie details and delete if found, else abort
        movie = Movie.query.get(movie_id)
        if movie:
            movie.delete()

            return jsonify({
                "success": True,
                "deleted_movie_id": movie_id
            })
        abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor():
        # parse json
        body = request.get_json()
        # check and extract headers
        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400)
        name = body['name']
        age = body['age']
        gender = body['gender']

        prior_actors_length = len(Actor.query.all())
        actor = Actor(name, age, gender)
        actor.insert()
        post_actors_length = len(Actor.query.all())
        # if an actor was inserted, then return json success else abort
        if post_actors_length > prior_actors_length:
            return jsonify({
                "success": True,
                "new_actor": actor.format()
            })
        abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movies():
        # parse json
        body = request.get_json()
        # check headers
        if 'title' not in body or 'release_date' not in body:
            abort(400)
        title = body['title']
        # parse and format dates
        release_date_list = body['release_date'].split('/')
        day = int(release_date_list[0])
        month = int(release_date_list[1])
        year = int(release_date_list[2])
        # validate dates
        if 1 <= day <= 31 and 1 <= month <= 12 and year < datetime.datetime.now().year + 1:
            release_date = datetime.date(year, month, day)
        else:
            abort(400)
        prior_movies_length = len(Movie.query.all())
        # insert movie
        movie = Movie(title, release_date)
        movie.insert()
        # if movie inserted successfully, return json success else abort
        post_movies_length = len(Movie.query.all())
        if post_movies_length > prior_movies_length:
            return jsonify({
                "success": True,
                "new_movie": movie.format()
            })
        abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id):
        # parse json
        body = request.get_json()
        # validate headers
        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400)
        # if actor id found, update details
        actor = Actor.query.get(actor_id)
        if actor:
            actor.name = body['name'] if body['name'] else actor.name
            actor.age = body['age'] if body['age'] else actor.age
            actor.gender = body['gender'] if body['gender'] else actor.gender

            actor.update()

            return jsonify({
                "success": True,
                "actor": actor.format()
            })
        abort(404)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id):
        # parse json
        body = request.get_json()
        # validate header
        if 'title' not in body or 'release_date' not in body:
            abort(400)
        # if movie id found, get details and update
        movie = Movie.query.get(movie_id)
        if movie:
            # parse and format dates
            release_date_list = body['release_date'].split('/')
            day = int(release_date_list[0])
            month = int(release_date_list[1])
            year = int(release_date_list[2])
            # validate dates and abort if invalid
            if 1 <= day <= 31 and 1 <= month <= 12 and year < datetime.datetime.now().year + 1:
                release_date = datetime.date(year, month, day)
            else:
                abort(400)

            movie.title = body['title'] if body['title'] else movie.title
            movie.release_date = release_date if release_date else movie.release_date

            movie.update()

            return jsonify({
                "success": True,
                "movie": movie.format()
            })
        abort(404)

    # Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'This method is not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': error.error
        }), error.status_code

    return app


# initialise and setup app
app = create_app()


if __name__ == '__main__':
    app.run()
