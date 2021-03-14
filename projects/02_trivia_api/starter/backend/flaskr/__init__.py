import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  
  def paginate_questions(selection, request):
      page = request.args.get('page',1, type=int)
      start = (page-1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      formatted_questions = [question.format() for question in selection]
      return formatted_questions[start:end]

  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.all()
    questions_on_page = paginate_questions(questions, request)
    categories = Category.query.all()
    if((len(questions_on_page) ==0) or (len(categories) ==0)):
        abort(404)
    else:
      return jsonify({'success':'True',
      'questions':questions_on_page,
      'total_questions':len(questions),
      'categories':[category.format() for category in categories],
      'current_category':None})

  @app.route('/categories', methods=['GET'])
  def get_catgories():
    categories = Category.query.all()
    if(len(categories)==0):
      abort(404)
    else:
      categories_dict = {}
      for category in categories:
        categories_dict[category.id] = category.type
      return jsonify({'success':'True',
      'categories':categories_dict,
      'total_categories':len(categories)})           

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id==question_id).one_or_none()
    if question is None:
      abort(404)
    else:
      try:
        question.delete()
        return jsonify({'success':'True',
        'question':question.format()}) 
      except:
        print(sys.exc_info())
        abort(422)
      
  @app.route('/questions', methods=['POST'])
  def question_submission():
    data = request.get_json()
    try:
      question = Question(question=data['question'], answer=data['answer'], category=data['category'], difficulty=data['difficulty'])
      question.insert()
      return jsonify({'success':'True',
            'created':question.id
            })
    except:
      print(sys.exc_info())
      abort(422)


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def question_search_category(category_id):
    category = Category.query.filter(Category.id==category_id).one_or_none()
    if(category is None):
      abort(404)
    else: 
      selection = Question.query.filter_by(category=str(category_id)).all()
      if(len(selection)==0):
        abort(404)
      else:
        formatted_questions = [question.format() for question in selection]
        return jsonify({'success':'True',
              'questions':formatted_questions,
              'total_questions': len(formatted_questions),
              'current_category': category.type})
    

  @app.route('/questions/search', methods=['POST'])
  def question_search():
    data = request.get_json()
    search_term = data.get('searchTerm','')
    selection = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
    if(len(selection)==0):
      abort(404)
    else:
      formatted_questions = [question.format() for question in selection]
      return jsonify({'success':'True',
            'questions':formatted_questions,
            'total_questions': len(selection),
            'current_category':None})
  
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    data = request.get_json()
    previous_questions = data['previous_questions']
    quiz_category = data['quiz_category']
    category_type = quiz_category.get('type')
    if(category_type=='click'):
      selection = Question.query.all()
    else:
      selection = Question.query.filter_by(category=str(quiz_category['id'])).all()
    if(len(selection)==0):
      abort(404)
    else:
      candidate_questions = []
      for question in selection:
        if question.id not in previous_questions:
          candidate_questions.append(question.format())
      if (len(candidate_questions)!=0):
        result = random.choice(candidate_questions)
        return jsonify({'success':'True',
            'question':result})
      else:
        return jsonify({'success':'False',
            'question':False})
      
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({'success':'False',
    'error':400,
    'message': "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({'success':'False',
    'error':404,
    'message': "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({'success':'False',
    'error':422,
    'message': "unprocessable"
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({'success':'False',
    'error':405,
    'message': "method is not allowed"
    }), 405

  @app.errorhandler(500)
  def method_not_allowed(error):
    return jsonify({'success':'False',
    'error':500,
    'message': "internal server error"
    }), 500

  return app

    