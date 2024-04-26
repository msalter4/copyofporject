from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'sceneseeker.db'

def create_app():
    # initializing Flask framework
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "key"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #f'sqlite:///{DB_NAME}'
    db.init_app(app) 

    # import all blueprints
    from .views import views
    from .auth import auth

    # now register these blueprints with the flask application
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app





