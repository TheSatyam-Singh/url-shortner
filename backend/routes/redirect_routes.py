from flask import Blueprint, redirect
from config import BASE_URL

redirect_bp = Blueprint("redirect", __name__)


@redirect_bp.route("/<short_code>")
def redirect_url(short_code):
    from app import mongo

    url_doc = mongo.db.urls.find_one({"short_code": short_code})
    if not url_doc:
        return "URL not found", 404

    mongo.db.urls.update_one(
        {"_id": url_doc["_id"]}, {"$inc": {"clicks": 1}}
    )
    return redirect(url_doc["original_url"])
