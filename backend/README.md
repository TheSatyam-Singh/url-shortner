# ShrinkEase - Backend

Flask API for the URL shortener service.

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Configuration

Create a `.env` file (optional):

```
MONGO_URI=mongodb://localhost:27017/urlshortner
SECRET_KEY=your-secret-key
BASE_URL=http://localhost:5000
```

## Run

```bash
python app.py
```

The server starts on `http://localhost:5000`.

## API Routes

### Auth
- `POST /api/auth/register` — Register a new user
- `POST /api/auth/login` — Login and get a token

### URLs (require Bearer token)
- `POST /api/shorten` — Shorten a URL
- `GET /api/urls` — List your URLs
- `DELETE /api/urls/<id>` — Delete a URL
- `GET /api/urls/<id>/stats` — Get URL stats

### Redirect
- `GET /<short_code>` — Redirect to the original URL

### Health
- `GET /api/health` — Health check
