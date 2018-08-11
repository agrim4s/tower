
from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# from flask_login import UserMixin
# from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

# from flask_dance.contrib.github import make_github_blueprint, github
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SECRET_KEY'] = 'key'
#app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
#github_blueprint = make_github_blueprint(client_id='',client_secret='')
# # app.register_blueprint(github_blueprint, url_prefix='http://gitlab.zycus.com/users/sign_in')
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

login_manager=LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from dynamic import routes
