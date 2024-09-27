from flask import Flask
from flask_migrate import Migrate
from models import db

def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.secret_key = '99090'
    db.init_app(app)
    migrate = Migrate(app,db)
    
    with app.app_context():
        db.create_all()

    return app