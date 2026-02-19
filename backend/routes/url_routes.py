import string
import random
import io
import base64
from datetime import datetime, timezone

import qrcode
from flask import Blueprint, request, jsonify, g
from bson.objectid import ObjectId
from auth import token_required
from config import BASE_URL

url_bp = Blueprint("url", __name__)


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def make_qr_base64(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


@url_bp.route("/shorten", methods=["POST"])
@token_required
def shorten_url():
    from app import mongo

    data = request.get_json()
    original_url = data.get("url", "").strip() if data else ""
    custom_code = data.get("custom_code", "").strip() if data else ""

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    if custom_code:
        if mongo.db.urls.find_one({"short_code": custom_code}):
            return jsonify({"error": "Custom code already taken"}), 409
        short_code = custom_code
    else:
        short_code = generate_short_code()
        while mongo.db.urls.find_one({"short_code": short_code}):
            short_code = generate_short_code()

    short_url = f"{BASE_URL}/{short_code}"
    qr_data = make_qr_base64(short_url)

    mongo.db.urls.insert_one(
        {
            "original_url": original_url,
            "short_code": short_code,
            "user_id": g.user_id,
            "clicks": 0,
            "created_at": datetime.now(timezone.utc),
            "qr_code": qr_data,
        }
    )

    return jsonify(
        {
            "short_url": short_url,
            "short_code": short_code,
            "original_url": original_url,
            "qr_code": qr_data,
        }
    ), 201


@url_bp.route("/urls", methods=["GET"])
@token_required
def get_user_urls():
    from app import mongo

    urls = list(mongo.db.urls.find({"user_id": g.user_id}))
    result = []
    for u in urls:
        result.append(
            {
                "id": str(u["_id"]),
                "original_url": u["original_url"],
                "short_code": u["short_code"],
                "short_url": f"{BASE_URL}/{u['short_code']}",
                "clicks": u.get("clicks", 0),
                "created_at": u.get("created_at", "").isoformat()
                if u.get("created_at")
                else "",
                "qr_code": u.get("qr_code", ""),
            }
        )
    return jsonify(result), 200


@url_bp.route("/urls/<url_id>", methods=["DELETE"])
@token_required
def delete_url(url_id):
    from app import mongo

    result = mongo.db.urls.delete_one(
        {"_id": ObjectId(url_id), "user_id": g.user_id}
    )
    if result.deleted_count == 0:
        return jsonify({"error": "URL not found"}), 404
    return jsonify({"message": "Deleted"}), 200


@url_bp.route("/urls/<url_id>/stats", methods=["GET"])
@token_required
def url_stats(url_id):
    from app import mongo

    url_doc = mongo.db.urls.find_one(
        {"_id": ObjectId(url_id), "user_id": g.user_id}
    )
    if not url_doc:
        return jsonify({"error": "URL not found"}), 404

    return jsonify(
        {
            "id": str(url_doc["_id"]),
            "original_url": url_doc["original_url"],
            "short_code": url_doc["short_code"],
            "short_url": f"{BASE_URL}/{url_doc['short_code']}",
            "clicks": url_doc.get("clicks", 0),
            "created_at": url_doc.get("created_at", "").isoformat()
            if url_doc.get("created_at")
            else "",
        }
    ), 200
