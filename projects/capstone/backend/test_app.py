import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from settings import *


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()
            new_actor = Actor('Bruce Banner', 50, 'Male')
            new_actor.insert()
            new_movie = Movie('LOTR', '10/12/2001')
            new_movie.insert()

            self.actor = {
                "name": 'Bruce Wayne',
                "age": 45,
                "gender": 'Male'
            }
            self.movie = {
                "title": "LOTR 2",
                "release_date": "11/12/2002"
            }
            self.actor_wrong_format = {
                "test": "This will fail"
            }
            self.movie_wrong_format = {
                "test": "This will fail"
            }

    # test endpoint success behaviour
    def test_get_actors(self):
        """Test all actors are retrieved"""
        res = self.client().get(
            '/actors', headers={'Authorization': f'Bearer {casting_assistant_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        """Test all movies are retrieved"""
        res = self.client().get(
            '/movies', headers={'Authorization': f'Bearer {casting_assistant_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_delete_actor(self):
        """Test actors can be deleted"""
        id = 1
        res = self.client().delete(
            f'/actors/{id}', headers={'Authorization': f'Bearer {casting_director_auth}'})
        data = json.loads(res.data)
        with self.app.app_context():
            actor = Actor.query.filter_by(id=id).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor_id'], id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(actor, None)

    def test_create_actor(self):
        """Test new actors can be created"""
        res = self.client().post('/actors', json=self.actor,
                                 headers={'Authorization': f'Bearer {casting_director_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actor'])

    def test_update_actor(self):
        """Test actors can be edited"""
        res = self.client().patch('/actors/1', json=self.actor,
                                  headers={'Authorization': f'Bearer {casting_director_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_movie(self):
        """Test movies can be deleted"""
        id = 1
        res = self.client().delete(
            f'/movies/{id}', headers={'Authorization': f'Bearer {executive_producer_auth}'})
        data = json.loads(res.data)
        with self.app.app_context():
            movie = Movie.query.filter_by(id=id).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie_id'], id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(movie, None)

    def test_create_movie(self):
        """Test new movies can be created"""
        res = self.client().post('/movies', json=self.movie,
                                 headers={'Authorization': f'Bearer {executive_producer_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movie'])

    def test_update_movie(self):
        """Test movies can be edited"""
        res = self.client().patch('/movies/1', json=self.movie,
                                  headers={'Authorization': f'Bearer {executive_producer_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # test end point failures

    def test_get_actors_fail(self):
        """Failed get actors request - no authorization"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message']['description'],
                         'Authorization not in header')

    def test_get_movies_fail(self):
        """Failed get movies request - no authorization"""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message']['description'],
                         'Authorization not in header')

    def test_delete_actor_fail(self):
        """Delete actors that don't exist"""
        id = 2000
        res = self.client().delete(
            f'/actors/{id}', headers={'Authorization': f'Bearer {casting_director_auth}'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie_fail(self):
        """Delete movies that don't exist"""
        id = 2000
        res = self.client().delete(
            f'/movies/{id}', headers={'Authorization': f'Bearer {executive_producer_auth}'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_actor_fail(self):
        """Create actor - unauthorized"""
        res = self.client().post("/actors", json=self.actor,
                                 headers={'Authorization': f'Bearer {casting_assistant_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')

    def test_create_new_movie_fail(self):
        """Create movie - unauthorized"""
        res = self.client().post("/movies", json=self.movie,
                                 headers={'Authorization': f'Bearer {casting_assistant_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')

    def test_create_new_actor_fail_2(self):
        """Create actor - wrong request body format"""
        res = self.client().post(
            "/actors", json=self.actor_wrong_format,
            headers={'Authorization': f'Bearer {executive_producer_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'bad request')

    def test_create_new_movie_fail_2(self):
        """Create movie - wrong request body format"""
        res = self.client().post(
            "/movies", json=self.movie_wrong_format,
            headers={'Authorization': f'Bearer {executive_producer_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'bad request')

    def test_update_new_actor_fail(self):
        """Updated actor - actor doesn't exist"""
        res = self.client().patch(
            "/actors/100", json=self.actor,
            headers={'Authorization': f'Bearer {casting_director_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_new_movie_fail(self):
        """Updated movie - movie doesn't exist"""
        res = self.client().patch(
            "/movies/100", json=self.movie,
            headers={'Authorization': f'Bearer {executive_producer_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_new_actor_fail_2(self):
        """Updated actor - wrong request body format"""
        res = self.client().patch(
            "/actors/1", json=self.actor_wrong_format,
            headers={'Authorization': f'Bearer {casting_director_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'bad request')

    def test_update_new_movie_fail_2(self):
        """Updated movie - wrong request body format"""
        res = self.client().patch(
            "/movies/1", json=self.movie_wrong_format,
            headers={'Authorization': f'Bearer {executive_producer_auth}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'bad request')

    def tearDown(self):
        """Executed after reach test"""
        pass


if __name__ == "__main__":
    unittest.main()
