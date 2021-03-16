import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

'''
Initial method to set up the application
'''


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    Setting up CORS. Allowing '*' for origins.
    '''
    CORS(app, resources={r"/": {"origins": "*"}})

    '''
    Using the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    Helper meethod for paginating questions
    '''
    def paginate_questions(selection, request):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in selection]
        return formatted_questions[start:end]

    '''
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()
        questions_on_page = paginate_questions(questions, request)
        categories = Category.query.all()
        if((len(questions_on_page) == 0) or (len(categories) == 0)):
            abort(404)
        else:
            return jsonify({'success': 'True',
                            'questions': questions_on_page,
                            'total_questions': len(questions),
                            'categories':
                            [category.format() for category in categories],
                            'current_category': None})

    '''
    Endpoint to handle GET requests
    for all available categories.
    This endpoint should return list of categories
    and not of categories
    '''
    @app.route('/categories', methods=['GET'])
    def get_catgories():
        categories = Category.query.all()
        if(len(categories) == 0):
            abort(404)
        else:
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type
            return jsonify({'success': 'True',
                            'categories': categories_dict,
                            'total_categories': len(categories)})

    '''
    Endpoint to DELETE question using a question ID.
    On success it returns deleted question
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        else:
            try:
                question.delete()
                return jsonify({'success': 'True',
                                'question': question.format()})
            except Exception as e:
                print(sys.exc_info())
                abort(422)

    '''
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    On success, it returns id of newly created
    question.
    '''
    @app.route('/questions', methods=['POST'])
    def question_submission():
        data = request.get_json()
        try:
            question = Question(question=data['question'],
                                answer=data['answer'],
                                category=data['category'],
                                difficulty=data['difficulty'])
            question.insert()
            return jsonify({'success': 'True',
                            'created': question.id
                            })
        except Exception as e:
            print(sys.exc_info())
            abort(422)
    '''
    Endpoint to get questions based on category.
    On success, it returns list of questions under passed
    category, no of total questions and current category.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def question_search_category(category_id):
        category = Category.query.filter(
            Category.id == category_id).one_or_none()
        if(category is None):
            abort(404)
        else:
            selection = Question.query.filter_by(
                category=str(category_id)).all()
            if(len(selection) == 0):
                abort(404)
            else:
                formatted_questions = [question.format()
                                       for question in selection]
                return jsonify({'success': 'True',
                                'questions': formatted_questions,
                                'total_questions': len(formatted_questions),
                                'current_category': category.type})
    '''
    POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    On success, it returns list of questions having that passed
    search term, no of such questions.
    '''
    @app.route('/questions/search', methods=['POST'])
    def question_search():
        data = request.get_json()
        search_term = data.get('searchTerm', '')
        selection = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))).all()
        if(len(selection) == 0):
            abort(404)
        else:
            formatted_questions = [question.format() for question in selection]
            return jsonify({'success': 'True',
                            'questions': formatted_questions,
                            'total_questions': len(selection),
                            'current_category': None})

    '''
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    On success, it returns a random question.
    '''
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        data = request.get_json()
        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']
        category_type = quiz_category.get('type')
        if(category_type == 'click'):
            selection = Question.query.all()
        else:
            selection = Question.query.filter_by(
                category=str(quiz_category['id'])).all()
        if(len(selection) == 0):
            abort(404)
        else:
            candidate_questions = []
            for question in selection:
                if question.id not in previous_questions:
                    candidate_questions.append(question.format())
            if (len(candidate_questions) != 0):
                result = random.choice(candidate_questions)
                return jsonify({'success': 'True',
                                'question': result})
            else:
                return jsonify({'success': 'False',
                                'question': False})
    '''
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': 'False',
                        'error': 400,
                        'message': "bad request"
                        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': 'False',
                        'error': 404,
                        'message': "resource not found"
                        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': 'False',
                        'error': 422,
                        'message': "unprocessable"
                        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'success': 'False',
                        'error': 405,
                        'message': "method is not allowed"
                        }), 405

    @app.errorhandler(500)
    def method_not_allowed(error):
        return jsonify({'success': 'False',
                        'error': 500,
                        'message': "internal server error"
                        }), 500

    return app
