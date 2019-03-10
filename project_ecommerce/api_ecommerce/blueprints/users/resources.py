import json
from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint, Flask
from . import *
from blueprints import db

from flask_jwt_extended import jwt_required, get_jwt_claims

bp_users = Blueprint('users', __name__)
api = Api(bp_users)

class UsersRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('first_name', location='json', required=True)
        parser.add_argument('last_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone', location='json', required=True)
        args = parser.parse_args()

        users = Users(None, args['username'], args['password'], args['first_name'], args['last_name'], args['email'], args['phone'])
        db.session.add(users)
        db.session.commit()

        if users is not None:
            return marshal(users, Users.response_field), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND', 'message': 'Users not found'}, 404, {'Content-Type': 'application/json'}

class UsersMe(Resource):
    @jwt_required
    def get(self):
        qry = Users.query.get(get_jwt_claims()['users_id'])
        if qry is not None:
            return marshal(qry, Users.response_field), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND', 'message': 'Users not found'}, 404, {'Content-Type': 'application/json'}


api.add_resource(UsersRegister, '/register')
api.add_resource(UsersMe, '/me')