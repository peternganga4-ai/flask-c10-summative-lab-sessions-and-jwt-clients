from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from extensions import db, bcrypt
from models import User

auth_bp = Blueprint("auth", __name__)


#register a new user

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")
    password_confirmation = data.get("password_confirmation", "")


    #validate input
    if not username or not password or not password_confirmation:
        return jsonify({
            "errors": ["All fields are required"]
        }), 400

    if len(password) < 8:
        return jsonify({
            "errors": ["Password must contain atleast 8 characters"]

        }), 400
    if password != password_confirmation:
        return jsonify({
            "errors": ["Passwords do not match"]
        }), 400

    #check whether username already exists
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({
            "errors": ["Username already exists"]
        }), 409

    #hash the password before storing it

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")


    new_user = User(
        username=username,
        password_hash=password_hash
    )

    db.session.add(new_user)
    db.session.commit()


    #Generate JWT token
    token = create_access_token(identity=str(new_user.id))

    return jsonify({
        "token": token,
        "user": new_user.to_dict()
    }), 201


#Login an existing user

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "errors": ["Username and password are required"]

        }), 400

    user = User.query.filter_by(username=username).first()

    #verify that the user exists and the password is correct
    if not user or not bcrypt.check_password_hash(
        user.password_hash, password
    ):
        return jsonify({
            "errors": ["Invalid username or password"]
        }), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "token": token,
        "user": user.to_dict()
    }), 200

# get the currently auth user
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "errors": ["User not found"]
        }), 404

    return jsonify(user.to_dict()), 200
