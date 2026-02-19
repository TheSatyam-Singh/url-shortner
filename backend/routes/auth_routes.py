from flask import Blueprint, request, jsonify
from auth import hash_password, check_password, create_token
from bson.objectid import ObjectId

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    from app import mongo

    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    existing = mongo.db.users.find_one({"username": data["username"]})
    if existing:
        return jsonify({"error": "Username already exists"}), 409

    hashed = hash_password(data["password"])
    result = mongo.db.users.insert_one(
        {"username": data["username"], "password": hashed}
    )
    token = create_token(result.inserted_id)
    return jsonify({"token": token, "username": data["username"]}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    from app import mongo

    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    user = mongo.db.users.find_one({"username": data["username"]})
    if not user or not check_password(data["password"], user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(user["_id"])
    return jsonify({"token": token, "username": user["username"]}), 200
