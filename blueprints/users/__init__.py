from flask_restful import fields
from blueprints import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(200))

    response_field = {
        'id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'phone': fields.String
    }

    def __init__(self, id, username, password, first_name, last_name, email, phone):
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f'<Users {self.id}>'

db.create_all()