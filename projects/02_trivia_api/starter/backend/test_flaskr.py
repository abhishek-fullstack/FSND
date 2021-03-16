import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://{}:{}@{}/{}'.format(
            'postgres', 'admin', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('questions'))
        self.assertIsNotNone(data.get('total_questions'))
        self.assertIsNotNone(data.get('categories'))
        self.assertIsNone(data.get('current_category'))

    def test_404_for_invalid_page_for_get_paginated_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertEqual(data['message'], "resource not found")
        self.assertIsNone(data.get('questions'))
        self.assertIsNone(data.get('total_questions'))
        self.assertIsNone(data.get('categories'))
        self.assertIsNone(data.get('current_category'))

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('total_categories'))
        self.assertIsNotNone(data.get('categories'))

    def test_404_for_malformed_path_for_get_categories(self):
        res = self.client().get('/categories/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('total_categories'))
        self.assertIsNone(data.get('categories'))
        self.assertEqual(data['message'], "resource not found")

    def test_delete_question(self):
        res = self.client().post(
            '/questions',
            json={
                'question': "Which city is capital of US",
                'answer': "Washington DC",
                'category': 3,
                'difficulty': 1})

        data = json.loads(res.data)

        res = self.client().delete('/questions/' + str(data.get('created')))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('question'))

    def test_404_for_invalid_question_for_delete_question(self):
        res = self.client().delete('/questions/450')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertEqual(data['message'], "resource not found")
        self.assertIsNone(data.get('question'))

    def test_post_question(self):
        res = self.client().post(
            '/questions',
            json={
                'question': "Which city is capital of US",
                'answer': "Washington DC",
                'category': 3,
                'difficulty': 1})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('created'))

    def test_422_incomplete_data_for_post_question(self):
        res = self.client().post(
            '/questions',
            json={
                'question': "Which city is capital of US",
                'answer': "Washington DC",
                'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('created'))

    def test_get_question_based_on_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('questions'))
        self.assertIsNotNone(data.get('total_questions'))
        self.assertEqual(data.get('current_category'), 'Art')

    def test_404_if_category_not_valid_for_get_question_based_on_category(
            self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('questions'))
        self.assertIsNone(data.get('total_questions'))
        self.assertIsNone(data.get('current_category'))

    def test_search_question_based_on_string(self):
        res = self.client().post(
            '/questions/search',
            json={
                'searchTerm': "Which"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('questions'))
        self.assertIsNotNone(data.get('total_questions'))
        self.assertIsNone(data.get('current_category'))

    def test_404_if_search_is_absent_for_search_question_based_on_string(self):
        res = self.client().post(
            '/questions/search',
            json={
                'searchTerm': "Ubiquitious"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('questions'))
        self.assertIsNone(data.get('total_questions'))
        self.assertIsNone(data.get('current_category'))

    def test_quiz(self):
        res = self.client().post(
            '/quizzes',
            json={
                'previous_questions': [14],
                'quiz_category': {
                    'type': 'Geography',
                    'id': '3'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertIsNotNone(data.get('question'))

    def test_404_if_category_is_invalid_for_quiz(self):
        res = self.client().post(
            '/quizzes',
            json={
                'previous_questions': [14],
                'quiz_category': {
                    'type': 'Mathematics',
                    'id': '14'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertIsNone(data.get('question'))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
