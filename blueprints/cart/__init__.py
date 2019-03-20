from flask import Blueprint, Flask
import json
from flask_restful import Resource, Api, reqparse, marshal
from . import *
from flask_restful import fields
from blueprints import db

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    total_qty = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    created_at = db.Column(db.String(200))
    deleted_at = db.Column(db.String(200))
    checkout = db.Column(db.String(200))

    response_field = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'total_qty': fields.Integer,
        'total_price': fields.Integer,
        'created_at': fields.String,
        'deleted_at': fields.String,
        'checkout': fields.String
    }

    def __init__(self, id, user_id, total_qty, total_price, created_at, deleted_at, checkout):
        self.id = id
        self.user_id = user_id
        self.total_qty = total_qty
        self.total_price = total_price
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.checkout = checkout

    def __repr__(self):
        return f'<Cart {self.id}>'

db.create_all()