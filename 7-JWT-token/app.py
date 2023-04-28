import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST

# sqlalchemy looks in models for __tablename__ to create tables
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


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

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or 'super-duper-secret'
    jwt = JWTManager(app)

    # jwt claims add additional info to tokens when they are created
    # check if user is admin
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {'is_admin': True}
        return {'is_admin': False}
    
    # check if token is in blocklist (which means user has logged out)
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    # jwt error handling
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {'description': 'The token has been revoked.', 'error': 'token_revoked'}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {'message': 'The token has expired.', 'error': 'token_expired'}
            ),
            401,
            )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {'message': 'Signature verification failed', 'error': 'invalid_token'}
            ),
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {'message': 'Signature verification failed.', 'error': 'invalid_token'}
            ),
            401,
        )
    
    # when a fresh token is required
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    'description': 'The token is not fresh',
                    'error': 'fresh_token_required',
                }
            ),
            401,
        )
    

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app