import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# define questions per page
QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'*': {'origins': '*'}})

    @app.after_request  # set access-control-allow control flow to run after each request
    def after_request(response):
        # allow certain request headers
        response.headers.add('Access-Control-Allow-Headers',
                             'Authorization, Content-Type')
        # allow certain request methods
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PUT, POST, PATCH, DELETE')

        return response

    # Create an endpoint to handle GET requests for all available categories.
    @app.route('/categories')
    def get_categories():

        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)

        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    # Create an endpoint to handle GET requests for questions including pagination
    @app.route('/questions')
    def get_questions():

        page = request.args.get('page', 1, type=int)
        questions = Question.query.order_by(Question.id.asc()).all()
        if len(questions) == 0:
            abort(404)

        questions_formatted = [question.format() for question in questions]
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': questions_formatted[start:end],
            'total_questions': len(questions),
            'current_category': None,
            'categories': categories_dict
        })

    # Create an endpoint to DELETE question using a question ID.
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter_by(id=question_id).one_or_none()

        if question:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        abort(404)

    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            new_question.insert()

            return jsonify({
                'success': True,
                'question': new_question.format()
            })
        except:
            abort(422)

    # Create a POST endpoint to get questions based on a search term.
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        # get search term from arguments
        search_term = body.get('searchTerm', '')
        # filter
        questions = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()
        # format
        questions = [question.format() for question in questions]
        if len(questions) != 0:
            return jsonify({
                'success': True,
                'questions': questions
            })
        abort(404)

    # Create a GET endpoint to get questions based on category.
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()

        if questions:
            questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': questions
            })
        abort(404)

    # Create a POST endpoint to get questions to play the quiz.
    @app.route('/quizzes', methods=['POST'])
    def quiz_questions():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        quiz_category = int(quiz_category['id'])

        questions = Question.query.filter_by(category=quiz_category).all()
        questions = [
            question for question in questions if question not in previous_questions]
        if len(questions) != 0:
            random_question = random.sample(questions, k=1)[0]

            return jsonify({
                'success': True,
                'question': random_question.format()
            })
        abort(404)

    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        })

    return app
