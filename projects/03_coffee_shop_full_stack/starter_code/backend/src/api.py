import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

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


db_drop_and_create_all()


# ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    if(len(drinks) == 0):
        abort(404)
    else:
        short_drinks = [drink.short() for drink in drinks]
        return jsonify({'success': 'True',
                        'drinks': short_drinks})


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()
    if(len(drinks) == 0):
        abort(404)
    else:
        long_drinks = [drink.long() for drink in drinks]
        return jsonify({'success': 'True',
                        'drinks': long_drinks})


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    data = request.get_json()
    try:
        drink = Drink(title=data['title'],
                      recipe=json.dumps(data['recipe']))
        drink.insert()
        return jsonify({'success': 'True',
                        'drinks': [drink.long()]
                        })
    except Exception as e:
        print(sys.exc_info())
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload, drink_id):
    drink = Drink.query.get(drink_id)
    data = request.get_json()
    if(drink is None):
        abort(404)
    else:
        title = data.get('title')
        recipe = data.get('recipe')
        if (title is not None):
            drink.title = title
        if (recipe is not None):
            drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify({'success': 'True',
                        'drinks': [drink.long()]
                        })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):
    drink = Drink.query.get(drink_id)
    if(drink is None):
        abort(404)
    else:
        drink.delete()
        return jsonify({'success': 'True',
                        'delete': drink_id
                        })

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': 'False',
                    'error': 404,
                    'message': "resource not found"
                    }), 404


@app.errorhandler(AuthError)
def auth_error_handle(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error['description']
    }), e.status_code
