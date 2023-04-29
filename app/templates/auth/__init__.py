from flask import Blueprint
app=Blueprint('app',__name__)
import app.templates.auth.views


from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'app.login'
def create_app(config_name):
     # ...
     login_manager.init_app(app)
