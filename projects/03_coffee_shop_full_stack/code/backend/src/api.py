import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    db_drop_and_create_all()

    # ROUTES
    '''
    implement endpoint
        GET /drinks
        public endpoint
        contains only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''


    @app.route('/drinks')
    def get_drinks():
        """Get drinks"""

        try:
            drinks = Drink.query.all()
            if drinks:
                drinks = [drink.short() for drink in drinks]
                return jsonify({
                    'success': True,
                    'drinks': drinks
                }), 200
        except:
            abort(404)


    '''
    implement endpoint
        GET /drinks-detail
        require the 'get:drinks-detail' permission
        contains the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks-detail')
    @requires_auth('get:drinks-detail')
    def get_drinks_detail():

        try:
            drinks = Drink.query.all()
            if drinks:
                drinks = [drink.long() for drink in drinks]
                return jsonify({
                    'success': True,
                    'drinks': drinks
                }), 200
        except:
            abort(404)

    '''
    implement endpoint
        POST /drinks
        create a new row in the drinks table
        require the 'post:drinks' permission
        contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def post_drinks():

        
        try:
            body = request.get_json()
            if 'title' not in body or 'recipe' not in body:
                abort(400)

            title = body['title']
            recipe = json.dumps(body['recipe'])
            new_drink = Drink(title=title, recipe=recipe)
            drinks = Drink.query.all()
            if new_drink not in drinks:
                new_drink.insert()

            return jsonify({
                'success': True,
                'drinks': new_drink.long()
            })
        except Exception:
            abort(422)


    '''
    implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            responds with a 404 error if <id> is not found
            update the corresponding row for <id>
            require the 'patch:drinks' permission
            contains the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks/<id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def edit_drink(id):

        body = request.get_json()
        if not body:
            abort(401)
        drink = Drink.query.get(id)
        if drink:
            if 'title' in body:
                title = body['title']
                drink.title = title
            if 'recipe' in body:
                recipe = str(list(body['recipe'].items()))
                drink.recipe = recipe
            drink.update()

            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            }), 200
        abort(404)


    '''
    implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            respond with a 404 error if <id> is not found
            delete the corresponding row for <id>
            require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks/<id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drink(id):

        drink = Drink.query.get(id)
        if drink:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        abort(404)


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
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': error.error
        }), error.status_code

    return app

