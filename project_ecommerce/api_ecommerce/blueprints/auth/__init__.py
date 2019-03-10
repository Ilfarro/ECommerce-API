from flask import Blueprint, Flask
import json
from flask_restful import Resource, Api, reqparse, marshal
from . import *
from blueprints.users import Users

from flask_jwt_extended import create_access_token

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResources(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        qry = Users.query.filter_by(username=args['username']).filter_by(password=args['password']).first()

        if qry is not None:
            token = create_access_token(identity=marshal(qry, Users.response_field))
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401
        return {'token': token}, 200

api.add_resource(CreateTokenResources, '')