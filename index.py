from flask import Flask
from flask_cors import CORS
from login import *
from google_login import *
from signup import *
from images import *
from optimize import *
from settings import *
from model import db
from main import *
from test_endpoint import *
from edit_user import *
from get_user import *
from delete_user import *
from logout import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECERET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
CORS(app)
db.init_app(app)
app.register_blueprint(hello_world_blueprint)
app.register_blueprint(test_post_blueprint)
app.register_blueprint(optimize_blueprint)
app.register_blueprint(get_images_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(google_login_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(get_blueprint)
app.register_blueprint(edit_blueprint)
app.register_blueprint(delete_blueprint)
app.register_blueprint(logout_blueprint)


if __name__ == '__main__':
    app.run()
