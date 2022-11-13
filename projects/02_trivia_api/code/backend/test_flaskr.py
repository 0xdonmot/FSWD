import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dbparams import dbparams


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}{}/{}".format(dbparams,
                                                           '@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "Is this a test question?",
                             "answer": "Yes", "category": 1, "difficulty": 1}

    def test_get_categories(self):
        """Test all categories are retrieved"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        """Test all questions are retrieved"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['questions']) <= 10)

    def test_delete_question(self):
        """Test questions can be deleted"""
        id = 2
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)
        question = Question.query.filter_by(id=id).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)

    def test_delete_question_fail(self):
        """Delete questions that don't exist"""
        id = 2e4
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)
        question = Question.query.filter_by(id=id).one_or_none()

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        """Test new questions can be created"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_create_new_question_fail(self):
        """Create question - wrong format"""
        res = self.client().post("/questions/10", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_search_question(self):
        """Search questions"""
        data = {'searchTerm': 'what'}
        res = self.client().post('/questions/search', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_search_question_not_found(self):
        """Search questions - not found"""
        data = {'searchTerm': 'This question will not be found'}
        res = self.client().post('/questions/search', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category(self):
        """Get questions by category"""
        id = 1
        res = self.client().get(f'/categories/{id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_get_questions_by_category_fail(self):
        """Get questions by category - Fail"""
        id = 1000
        res = self.client().get(f'/categories/{id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz_questions(self):
        """Get quiz questions"""
        data = {
            'quiz_category': {'type': 'Geography', 'id': '3'},
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        # 5 items in one formatted question object
        self.assertEqual(len(data['question']), 5)

    def test_get_quiz_questions_fail(self):
        """Get quiz questions - fail"""
        data = {
            'quiz_category': {'type': 'Geography', 'id': '1000'},
            'previous_questions': []
        }

        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def tearDown(self):
        """Executed after reach test"""
        pass


if __name__ == "__main__":
    unittest.main()
