from flask import Flask
from redis import Redis
import sys 
import os



from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
def create_app(config_name):
     # ...
     from .auth import auth as auth_blueprint
     app.register_blueprint(auth_blueprint, url_prefix='/auth')
     return app




