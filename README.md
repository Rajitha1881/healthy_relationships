# Healthy Relationships API & Library

This repository deals with entire SDLC practice starting from writing Python code to API deployment and CI/CD testing.

## Project Structure

- [`relationship_messages.py`](relationship_messages.py): Core module containing relationship messages, retrieval functions, and CLI execution.
- [`app.py`](app.py): REST API built with FastAPI exposing endpoints for messages and categories.
- [`test_relationship_messages.py`](test_relationship_messages.py): Unit tests for the core Python functions.
- [`test_app.py`](test_app.py): Integration and unit tests for the FastAPI web endpoints.
- [`requirements.txt`](requirements.txt): Pinned dependencies for the environment.

---

## 1. Setup Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Running the API Web Server

Start the FastAPI application with Uvicorn:

```bash
python3 app.py
```
Or:
```bash
uvicorn app:app --reload
```

The server runs at `http://127.0.0.1:8000`.

---

## 3. Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 4. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root / API health status and endpoint list |
| `GET` | `/categories` | Returns all available message categories |
| `GET` | `/message` | Returns a random message (or filter with `?category=growth`) |
| `GET` | `/message/{category}` | Returns a message for a specific category (e.g. `/message/growth`) |
| `POST` | `/message` | Accepts JSON `{"category": "growth"}` in the request body |

### Examples with `curl`:

```bash
# 1. Get available categories
curl http://127.0.0.1:8000/categories

# 2. Get a random message
curl http://127.0.0.1:8000/message

# 3. Get a message from the 'growth' category (Query Param)
curl http://127.0.0.1:8000/message?category=growth

# 4. Get a message from the 'communication' category (Path Param)
curl http://127.0.0.1:8000/message/communication

# 5. POST request with JSON payload
curl -X POST http://127.0.0.1:8000/message \
  -H "Content-Type: application/json" \
  -d '{"category": "boundaries"}'
```

---

## 5. Running Tests

Run all unit and API tests with:

```bash
python3 -m unittest discover -v
```
