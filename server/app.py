from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db, migrate, bcrypt, jwt


def create_app(config_class=Config):
    app = Flask(__name__)

    #load application configuration
    app.config.from_object(config_class)

    #initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def handle_missing_token(error):
        return jsonify({"errors": [error]}), 401

    @jwt.invalid_token_loader
    def handle_invalid_token(error):
        return jsonify({"errors": [error]}), 422

    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        return jsonify({"errors": ["Token has expired"]}), 401
    

    #allow our react frontend to communicate with flask

    CORS(app, resources={
        r"/*": {"origins": "http://localhost:4000"}
    })

    #import models so SQLAlchemy and migrations can discover them
    from models import User, Note

    #register API resources
    from resources.auth import auth_bp
    from resources.notes import notes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    #handle common errors using the frontend's expected format
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"errors": ["Resource not found"]}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"errors": ["Bad request"]}), 400

    @app.route("/")
    def home():
        return jsonify({
            "message": "Productivity App API is running"
        }), 200

    return app

app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
