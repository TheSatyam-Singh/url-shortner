import os

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from config import MONGO_URI, SECRET_KEY

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
app.config["SECRET_KEY"] = SECRET_KEY

CORS(app)
mongo = PyMongo(app)

from routes.auth_routes import auth_bp
from routes.url_routes import url_bp
from routes.redirect_routes import redirect_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(url_bp, url_prefix="/api")
app.register_blueprint(redirect_bp)


@app.route("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", port=5000)
