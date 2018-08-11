import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.case import Case, CaseList
from resources.library import Library, LibraryList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'spynos'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Library, '/library/<string:name>')
api.add_resource(LibraryList, '/libraries')
api.add_resource(Case, '/case/<string:name>')
api.add_resource(CaseList, '/cases')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
