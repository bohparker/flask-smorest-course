import os
from flask import Flask
from flask_smorest import Api

from db import db

# sqlalchemy looks in models for __tablename__ to create tables
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


# create an app factory function that takes in db url param for testing
def create_app(db_url=None):
    app = Flask(__name__)
    # when an exception is raise in an extension, it is brought to the Flask app
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # use db_url from param or env var or default=sqlite file in current directory
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
    # will soon be deprecated fro sqlalchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app