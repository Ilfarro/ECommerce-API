from flask import Flask, request
from flask_restful import Api
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

# CONNECTION STRING
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ilham:alphatech123@172.31.38.74:3306/e_commerce'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alphatech123@localhost:3306/e_commerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# FOR JWT MANAGER
app.config['JWT_SECRET_KEY'] = '12345678'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

# MIDDLE WARE UNTUK DAPATKAN IDENTITY
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

db.create_all()

# initiate flask-restful instance
api = Api(app, catch_all_404s=True)

## MIDDLE WARE
@app.after_request
def after_request(response):
    if request.method == 'GET':
        app.logger.warning("REQUEST_LOG\t%s %s %s %s", response.status_code, request.method, request.url, json.dumps({ 'request': request.args.to_dict(), 'response': json.loads(response.data.decode('utf-8')) }))
    else:
        app.logger.warning("REQUEST_LOG\t%s %s %s %s", response.status_code, request.method, request.url, json.dumps({ 'request': request.get_json(), 'response': json.loads(response.data.decode('utf-8')) }))
    return response

# CALL BLUEPRINT
from blueprints.auth import bp_auth
from blueprints.users.resources import bp_users
from blueprints.items.resources import bp_items
from blueprints.cart import bp_cart

#JIKA INGIN MERUBAH PREFIX TAMBAHKAN (url_prefix='....')
app.register_blueprint(bp_auth, url_prefix='/api/users/login')
app.register_blueprint(bp_users, url_prefix='/api/users')
app.register_blueprint(bp_items, url_prefix='/api')