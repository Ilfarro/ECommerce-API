import json
from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint, Flask
from . import *
from blueprints.users import *
from blueprints import db

from flask_jwt_extended import jwt_required, get_jwt_claims

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)
class ItemsAuthenticated(Resource):
    @jwt_required
    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('search', location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']  

            qry = Items.query

            if args['search'] is not None:
                qry = qry.filter(Items.kategori.like("%"+args['search']+"%"))
                if qry.first() is None:
                    qry = Items.query.filter(Items.nama.like("%"+args['search']+"%"))
                    if qry.first() is None:
                        qry = Items.query.filter(Items.deskripsi.like("%"+args['search']+"%"))
                        if qry.first() is None:
                            qry = Items.query.filter(Items.lokasi.like("%"+args['search']+"%"))
                            if qry.first() is None:
                                return {'status': 'NOT_FOUND', 'message': 'Items not found'}, 404, {'Content-Type': 'application/json'}

            

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Items.response_field))
            return rows, 200, {'Content-Type': 'application/json'}

        else:
            qry = Items.query.get(id)
            if qry is not None:
                return marshal(qry, Items.response_field), 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'Items not found'}, 404, {'Content-Type': 'application/json'}

    @jwt_required
    def post(self):
        users_id = get_jwt_claims()["id"]
        parser = reqparse.RequestParser()
        parser.add_argument('kategori', location='json', required=True)
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('deskripsi', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        parser.add_argument('lokasi', location='json', required=True)
        parser.add_argument('url_foto', location='json', required=True)
        args = parser.parse_args()

        items = Items(None, args['kategori'], args['nama'], args['deskripsi'], args['harga'], args['lokasi'], args['url_foto'], users_id)
        db.session.add(items)
        db.session.commit()

        if items is not None:
            return marshal(items, Items.response_field), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND', 'message': 'Items not found'}, 404, {'Content-Type': 'application/json'}
        
    @jwt_required
    def patch(self, id):
        qry = Items.query.get(id)
        # temp = marshal(qry, Items.response_field)
        
        parser = reqparse.RequestParser()
        parser.add_argument('kategori', location='json')
        parser.add_argument('nama', location='json')
        parser.add_argument('deskripsi', location='json')
        parser.add_argument('harga', location='json')
        parser.add_argument('lokasi', location='json')
        parser.add_argument('url_foto', location='json')
        args = parser.parse_args()

        if args['kategori'] is not None:
            qry.kategori = args['kategori']
        if args['nama'] is not None:
            qry.nama = args['nama']
        if args['deskripsi'] is not None:
            qry.harga = args['deskripsi']
        if args['harga'] is not None:
            qry.harga = args['harga']
        if args['lokasi'] is not None:
            qry.lokasi = args['lokasi']
        if args['url_foto'] is not None:
            qry.url_foto = args['url_foto']

        db.session.commit()

        if qry is not None:
            return marshal(qry, Items.response_field), 200, {'Content-Type': 'application/json'}
        return {'status': 'NOT_FOUND', 'message': 'Items not found'}, 404, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, id):
        qry = Items.query.get(id)
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return "deleted", 200
        return {'status': 'NOT_FOUND', 'message': 'Items not found'}, 404, {'Content-Type': 'application/json'}
        
class ItemsPublic(Resource):
    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('search', location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']  
            
            qry = Items.query

            if args['search'] is not None:
                qry = qry.filter(Items.kategori.like("%"+args['search']+"%"))
                if qry.first() is None:
                    qry = Items.query.filter(Items.nama.like("%"+args['search']+"%"))
                    if qry.first() is None:
                        qry = Items.query.filter(Items.deskripsi.like("%"+args['search']+"%"))
                        if qry.first() is None:
                            qry = Items.query.filter(Items.lokasi.like("%"+args['search']+"%"))
                            if qry.first() is None:
                                return {'status': 'NOT_FOUND', 'message': 'Items not found'}, 404, {'Content-Type': 'application/json'}

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Items.response_field))
            return rows, 200, {'Content-Type': 'application/json'}

        else:
            qry = Items.query.get(id)
            if qry is not None:
                return marshal(qry, Items.response_field), 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'Items not found'}, 404, {'Content-Type': 'application/json'}

api.add_resource(ItemsAuthenticated, '/users/items', '/users/items/<int:id>')
api.add_resource(ItemsPublic, '/public/items', '/public/items/<int:id>')