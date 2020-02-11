import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from database.models import db_drop_and_create_all, setup_db, Movie, Actor
from controllers.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
# Set up cors and allow '*' for origins
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# MOVIE ROUTES

# Handle GET requests for all available movies.
@app.route('/movies')
@cross_origin()
def get_all_movies():
    movies = Movie.query.all()
    try:
        movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': movies
        }), 200
    except Exception:
        abort(500)

# Handle endpoint to POST a new movie
@app.route('/movies', methods=['POST'])
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
@app.route('/movies/<int:id>', methods=['PATCH'])
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
@app.route('/movies/<int:id>', methods=['DELETE'])
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
