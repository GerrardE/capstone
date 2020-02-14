import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import db_drop_and_create_all, setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres:1234@localhost:5432', self.database_name)
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

        self.executive_producer_token = ""

        self.headers = {
            'Content-Type': 'application/json', 
            'Token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9VWXpRVFJGUVRNM01FSXlSakJDTlRCQlJVVkZORFJFTnpZNU1rSXdPRGczT1RRM09UUXhOUSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWFwcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0MzA1NmY4ODYwYzgwZTg5ZGIwYzI5IiwiYXVkIjoiYXV0aCIsImlhdCI6MTU4MTY3NDk1OSwiZXhwIjoxNTgxNjgyMTU5LCJhenAiOiJ0cUZJbVRTWGZBZlN1MW1OcTlrcW5VdWhHckhLczFsciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.PAnQMleGMjUOez7CTi9B3wrzGAmM46SWtiVl0DhA08_cf3jXE_7FLbsLLlVyUZnZW6rud-nnTwT1RoNR794oI9dqPvAbboCKzE7KyJmrpJVylAEFRedkTMNTo_Lx9QElG3O2qMRmxeiddsMX5Yv_NDXpPJF3IV3ycw2JA06no2jOPYTcVlXFg0Uol99T3d5vKVGRtglDbi1WreqWnbVOb8ZnhABvXm9yCz9CqCU6Y6YgZkxC0IaNL5zrL1eq5NUMHHTF7L9uLrbQYyEnZbhwmdYEaPwpgoJK0p5RjJ5X7Cb5eCofLnbK-E31R_7Xtbw_dIuKg1Y2pF1UVUlbnXaCjQ'
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Handle GET requests
    def test_get_all_movies(self):
        res = self.client().get('/api/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_all_actors(self):
        res = self.client().get('/api/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Handle POST requests
    def test_post_a_movie(self):
        res = self.client().post('/api/movies', headers=self.headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_an_actor(self):
        res = self.client().post('/api/actors', headers=self.headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Handle PATCH requests.
    def test_patch_a_movie(self):
        res = self.client().patch('/api/movies/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_an_actor(self):
        res = self.client().patch('/api/actors/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Handle DELETE requests.
    def test_delete_a_movie(self):
        res = self.client().delete('/api/movies/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_an_actor(self):
        res = self.client().delete('/api/actors/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
