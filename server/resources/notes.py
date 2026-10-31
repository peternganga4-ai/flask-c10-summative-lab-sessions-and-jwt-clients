from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Note

notes_bp = Blueprint("notes", __name__)

#get all notes belonging to the logged-in user
@notes_bp.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    user_id = int(get_jwt_identity())

    #get pagination parameters
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
    except (ValueError, TypeError):
        return jsonify({
            "errors": ["Page and per_page must be valid numbers"]

        }), 400


    if page < 1 or per_page < 1 or per_page > 100:
        return jsonify({
            "errors": ["Invalid pagination parameters"]
        }), 400

    if page < 1 or per_page < 1 or per_page > 100:
        return jsonify({
            "errors": ["Invalid pagination parameters"]
        }), 400

    #Only retrieve notes belonging to the logged-in user
    pagination = Note.query.filter_by(
        user_id=user_id
    ).order_by(
        Note.created_at.desc
        ()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "notes": [note.to_dict() for note in pagination.items], "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_notes": pagination.total,
            "total_pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_previous": pagination.has_prev
        }

    }), 200


#create a note
@notes_bp.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    user_id = int(get_jwt_identity())

    data = request.get_json(silent=True) or {}

    title = data.get("title", "")
    content = data.get("content", "")

    if not isinstance(title, str) or not isinstance(content, str):
        return jsonify({
            "errors": ["Title and content must be text"]
        }), 400

    title = title.strip()
    content = content.strip()


    if not title or not content:
        return jsonify({
            "errors": ["Title and content are required"]
        }), 400


    new_note = Note(
        title=title,
        content=content,
        user_id=user_id

    )

    db.session.add(new_note)
    db.session.commit()

    return jsonify(new_note.to_dict()), 201


#get a single note
@notes_bp.route("/notes/<int:note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id):
    user_id = int(get_jwt_identity())


    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()


    if not note:
        return jsonify({
            "errors": ["Note not found"]
        }), 404

    return jsonify(note.to_dict()), 200

# update a note
@notes_bp.route("/notes/<int:note_id>", methods=["PATCH"])
@jwt_required()
def update_note(note_id):
    user_id = int(get_jwt_identity())

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

    if not note:
        return jsonify({
            "errors": ["Note not found"]
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "errors": ["Provide at least one field to update"]
        }), 400

    allowed_fields = {"title", "content"}

    if not set(data.keys()).issubset(allowed_fields):
        return jsonify({
            "errors": ["Only title and content can be updated"]
        }), 400

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return jsonify({
                "errors": ["Title cannot be empty"]
            }), 400

        note.title = data["title"].strip()

    if "content" in data:
        if not isinstance(data["content"], str) or not data["content"].strip():
            return jsonify({
                "errors": ["Content cannot be empty"]
            }), 400

        note.content = data["content"].strip()

    db.session.commit()

    return jsonify(note.to_dict()), 200
# delete a note
@notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    user_id = int(get_jwt_identity())

    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()


    if not note:
        return jsonify({
            "errors": ["Note not found"]
        }), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "message": "Note deleted successfully"
    }), 200
