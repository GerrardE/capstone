import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from database.models import setup_db, Movie, Actor

load_dotenv()


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = os.getenv('TEST_DATABASE_URL')
        setup_db(self.app, self.database_path)

        self.new_movie = {
            "title": "The first time",
            "release_date": "9-Aug-2018",
        }

        self.new_actor = {
            "name": "John Doe",
            "gender": "male",
            "age": "30"
        }

        self.assistant_headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv('CASTING_ASSISTANT')
        }

        self.director_headers = {
            "Content-Type": "application/json",
            "Authorization":  os.getenv('CASTING_DIRECTOR')
        }

        self.producer_headers = {
            "Content-Type": "application/json",
            "Authorization":  os.getenv('EXECUTIVE_PRODUCER')
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create/drop all tables

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Handle GET requests
    def test_get_all_movies(self):
        res = self.client().get('/api/movies', headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_all_actors(self):
        res = self.client().get('/api/actors', headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Handle POST requests
    def test_add_a_movie(self):
        res = self.client().post(
            '/api/movies', headers=self.producer_headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_an_actor(self):
        res = self.client().post(
            '/api/actors', headers=self.producer_headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Handle EDIT requests.
    def test_edit_a_movie(self):
        movie = {
            "title": "Smart Man",
            "release_date": "9-Feb-2020",
        }
        res = self.client().patch('/api/movies/1',
                                  headers=self.producer_headers, json=movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_an_actor(self):
        actor = {
            "name": "Dame Janel",
            "gender": "female",
            "age": "23"
        }
        res = self.client().patch('/api/actors/1',
                                  headers=self.producer_headers, json=actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Handle DELETE requests.
    def test_remove_a_movie(self):
        res = self.client().delete('/api/movies/2',
                                   headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_remove_an_actor(self):
        res = self.client().delete('/api/actors/2',
                                   headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # HANDLE ERRORS

    # Handle ERROR ON GET requests

    def test_fail_get_all_movies(self):
        res = self.client().get('/api/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unauthorized client error")
        self.assertEqual(data['success'], False)

    def test_fail_get_all_actors(self):
        res = self.client().get('/api/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unauthorized client error")
        self.assertEqual(data['success'], False)

    # Handle ERROR ON POST requests
    def test_fail_add_a_movie(self):
        res = self.client().post('/api/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unauthorized client error")
        self.assertEqual(data['success'], False)

    def test_fail_add_an_actor(self):
        res = self.client().post('/api/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unauthorized client error")
        self.assertEqual(data['success'], False)

    # Handle ERROR ON EDIT requests.
    def test_fail_edit_a_movie(self):
        movie = {
            "title": "Smart Man",
            "release_date": "9-Feb-2020",
        }
        res = self.client().patch('/api/movies/1', json=movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unauthorized client error")
        self.assertEqual(data['success'], False)

    def test_fail_edit_an_actor(self):
        actor = {
            "name": "Dame Janel",
            "gender": "female",
            "age": "23"
        }
        res = self.client().patch('/api/actors/1', json=actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unauthorized client error")
        self.assertEqual(data['success'], False)

    # Handle ERROR ON DELETE requests.
    def test_fail_remove_a_movie(self):
        res = self.client().delete('/api/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unauthorized client error")
        self.assertEqual(data['success'], False)

    def test_fail_remove_an_actor(self):
        res = self.client().delete('/api/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unauthorized client error")
        self.assertEqual(data['success'], False)

    # RBAC TESTS

    # EXECUTIVE PRODUCER
    # Handle ERROR ON DELETE requests.

    def test_error_remove_a_movie(self):
        res = self.client().delete('/api/movies/500',
                                   headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_error_remove_an_actor(self):
        res = self.client().delete('/api/actors/200',
                                   headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    # CASTING ASSISTANT
    # Handle GET requests

    def test_get_movies(self):
        res = self.client().get('/api/movies',
                                headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors(self):
        res = self.client().get('/api/actors',
                                headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # CASTING DIRECTOR
    # Handle ERROR ON PATCH requests
    def test_error_edit_a_movie(self):
        movie = {
            "title": "Smart Man",
            "release_date": "9-Feb-2020",
        }
        res = self.client().patch('/api/movies/100',
                                  headers=self.director_headers, json=movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_error_edit_an_actor(self):
        actor = {
            "name": "Dame Janel",
            "gender": "female",
            "age": "23"
        }
        res = self.client().patch('/api/actors/100',
                                  headers=self.director_headers, json=actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
