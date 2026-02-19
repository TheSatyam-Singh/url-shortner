import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/urlshortner")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
