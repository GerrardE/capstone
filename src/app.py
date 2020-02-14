import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from database.models import db_drop_and_create_all, setup_db, Movie, Actor
from controllers.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    # Set up cors and allow '*' for origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,PUT,DELETE,OPTIONS')
        return response

    '''
    uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()

    # MOVIE ROUTES

    # Handle GET requests for all available movies.
    @app.route('/api/movies')
    @cross_origin()
    @requires_auth('view:movies')
    def get_all_movies(jwt):
        movies = Movie.query.all()
        print(movies)
        try:
            movies = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': movies
            }), 200
        except Exception:
            abort(500)

    # Handle endpoint to POST a new movie
    @app.route('/api/movies', methods=['POST'])
    @cross_origin()
    @requires_auth('post:movies')
    def post_movie(jwt):
        # Declare and empty data dictionary to hold all retrieved variables
        data = request.get_json()

        # set movie variable equal to corresponding model class,
        # ready for adding to the session
        movie = data.get('movie')

        movie = Movie(
            title=data.get('title'),
            release_date=data.get('release_date')
        )

        try:
            movie.insert()
        except Exception:
            abort(400)

        movies = Movie.query.all()
        try:
            movies = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': movies
            }), 200
        except Exception:
            abort(500)

    # Handle endpoint to PATCH an existing movie
    @app.route('/api/movies/<int:id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth('patch:movies')
    def patch_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        # Declare and empty data dictionary to hold all retrieved variables
        data = request.get_json()

        # set movie variable equal to corresponding model class,
        # ready for adding to the session

        title = data.get('title')
        release_date = data.get('release_date')

        try:
            movie.title = title
            movie.release_date = release_date
            movie.update()
        except Exception:
            abort(422)

        movies = Movie.query.all()
        try:
            movies = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': movies
            }), 200
        except Exception:
            abort(500)

    # Handle endpoint to DELETE an existing movie
    @app.route('/api/movies/<int:id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()
        except Exception:
            abort(422)

        movies = Movie.query.all()
        try:
            movies = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': movies
            }), 200
        except Exception:
            abort(500)

    # ACTOR ROUTES

    # Handle GET requests for all available actors.
    @app.route('/api/actors')
    @cross_origin()
    @requires_auth('view:actors')
    def get_all_actors(jwt):
        actors = Actor.query.all()
        try:
            actor = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': actor
            }), 200
        except Exception:
            abort(500)

    # Handle endpoint to POST a new actor
    @app.route('/api/actors', methods=['POST'])
    @cross_origin()
    @requires_auth('post:actors')
    def post_actor(jwt):
        # Declare and empty data dictionary to hold all retrieved variables
        data = request.get_json()

        # set actor variable equal to corresponding model class,
        # ready for adding to the session
        actor = data.get('actor')

        actor = Actor(
            name=data.get('name'),
            age=data.get('age'),
            gender=data.get('gender')
        )

        try:
            actor.insert()
        except Exception:
            abort(400)

        actors = Actor.query.all()
        try:
            actors = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': actors
            }), 200
        except Exception:
            abort(500)

    # Handle endpoint to PATCH an existing actor
    @app.route('/api/actors/<int:id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth('patch:actors')
    def patch_actor(jwt, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        # Declare and empty data dictionary to hold all retrieved variables
        data = request.get_json()

        # set actor variable equal to corresponding model class,
        # ready for adding to the session

        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')

        try:
            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.update()
        except Exception:
            abort(422)

        actors = Actor.query.all()
        try:
            actors = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': actors
            }), 200
        except Exception:
            abort(500)

    # Handle endpoint to DELETE an existing actor
    @app.route('/api/actors/<int:id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()
        except Exception:
            abort(422)

        actors = Actor.query.all()
        try:
            actors = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': actors
            }), 200
        except Exception:
            abort(500)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable_req(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable request"
        }), 422

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def failed_req(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "request failed"
        }), 400

    # handle unauthorized client error
    @app.errorhandler(AuthError)
    def unauthorized_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized client error",
        }), 401

    # handle unauthorized client error
    @app.errorhandler(401)
    def unauthorized_req(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized client error",
        }), 401

    # handle forbidden errors
    @app.errorhandler(403)
    def forbidden_req(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden request. Please contact your administrator.",
        }), 403

    # handle server errors
    @app.errorhandler(500)
    def server_err(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error.",
        }), 500

    return app
