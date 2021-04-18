import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import setup_db, db_drop_and_create_all


class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    ca_token = os.environ['CASTING_ASSISTANT_TOKEN']
    cd_token = os.environ['CASTING_DIRECTOR_TOKEN']
    ep_token = os.environ['EXECUTIVE_PRODUCER_TOKEN']

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            'postgres', 'admin', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # db_drop_and_create_all()
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('actors'))
        self.assertIsNotNone(data.get('total_actors'))

    def test_auth_error_without_token_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('actors'))
        self.assertIsNone(data.get('total_actors'))

    def test_get_actor_detail(self):
        res = self.client().get(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('actor'))

    def test_404_for_invalid_actor_for_get_actor_detail(self):
        res = self.client().get(
            '/actors/102',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('actor'))

    def test_auth_error_wrong_token_get_actor_detail(self):
        res = self.client().get(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format("wrong_token")})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('actor'))

    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/3',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('deleted_actor'))

    def test_404_for_invalid_actor_for_delete_actor(self):
        res = self.client().delete(
            '/actors/102',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('deleted_actor'))

    def test_auth_error_less_permitted_token_delete_actor(self):
        res = self.client().delete(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('deleted_actor'))

    def test_create_actor(self):
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)},
            json={
                "name": "Amitabh Bachchan",
                "nationality": "Indian",
                "date_of_birth": "12-oct-1943"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('created_actor'))

    def test_422_for_no_name_for_create_actor(self):
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)},
            json={
                "nationality": "Indian",
                "date_of_birth": "12-oct-1943"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('created_actor'))

    def test_auth_error_less_permitted_token_create_actor(self):
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)},
            json={
                "name": "Amitabh Bachchan",
                "nationality": "Indian",
                "date_of_birth": "12-oct-1943"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('created_actor'))

    def test_update_actor(self):
        res = self.client().patch(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)},
            json={
                "name": "Amitabh Bachchan Senior",
                "movies": [1]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('updated_actor'))

    def test_422_for_invalid_movies_for_update_actor(self):
        res = self.client().patch(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)},
            json={
                "name": "Amitabh Bachchan Senior",
                "movies": [
                    1,
                    50]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('updated_actor'))

    def test_auth_error_less_permitted_token_update_actor(self):
        res = self.client().patch(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)},
            json={
                "name": "Amitabh Bachchan Senior",
                "movies": [1]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('updated_actor'))

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('movies'))
        self.assertIsNotNone(data.get('total_movies'))

    def test_auth_error_without_token_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('movies'))
        self.assertIsNone(data.get('total_movies'))

    def test_get_movie_detail(self):
        res = self.client().get(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('movie'))

    def test_404_for_invalid_movie_for_get_movie_detail(self):
        res = self.client().get(
            '/movies/102',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('movie'))

    def test_auth_error_wrong_token_get_movie_detail(self):
        res = self.client().get(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format("wrong token")})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('movie'))

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/2',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ep_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('deleted_movie'))

    def test_404_for_invalid_actor_for_delete_movie(self):
        res = self.client().delete(
            '/movies/102',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ep_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('deleted_movie'))

    def test_auth_error_less_permitted_token_delete_movie(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('deleted_movie'))

    def test_create_movie(self):
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ep_token)},
            json={
                "name": "World Day",
                "genre": "Western",
                "language": "French",
                "year": "2022",
                "imdb_rating": "0"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('created_movie'))

    def test_422_for_no_name_for_create_movie(self):
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ep_token)},
            json={
                "genre": "Western",
                "language": "French",
                "year": "2022",
                "imdb_rating": "0"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('created_movie'))

    def test_auth_error_less_permitted_token_create_movie(self):
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)},
            json={
                "name": "World Day",
                "genre": "Western",
                "language": "French",
                "year": "2022",
                "imdb_rating": "0"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('created_movie'))

    def test_update_movie(self):
        res = self.client().patch(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)},
            json={
                "name": "Name updated",
                "actors": [1]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('updated_movie'))

    def test_422_for_invalid_actors_for_update_movie(self):
        res = self.client().patch(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.cd_token)},
            json={
                "name": "Name updated",
                "actors": [
                    1,
                    102]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('updated_movie'))

    def test_auth_error_less_permitted_token_update_actor(self):
        res = self.client().patch(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.ca_token)},
            json={
                "name": "Name updated",
                "actors": [1]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('updated_movie'))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
