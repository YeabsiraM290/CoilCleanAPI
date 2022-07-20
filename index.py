from flask import Flask
from flask_cors import CORS
from .apps.auth import *
from .apps.auth import logout_blueprint
from .apps.auth.google_login import *
from .apps.views.images import *
from .apps.views.optimize import *
from .settings import *
from .database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
CORS(app)
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
