# Healthy Relationships API & Library

This repository deals with entire SDLC practice starting from writing Python code to API deployment and CI/CD testing.

## Project Structure

- [`relationship_messages.py`](relationship_messages.py): Core module containing relationship messages, retrieval functions, and CLI execution.
- [`app.py`](app.py): REST API built with FastAPI exposing endpoints for messages and categories.
- [`test_relationship_messages.py`](test_relationship_messages.py): Unit tests for the core Python functions.
- [`test_app.py`](test_app.py): Integration and unit tests for the FastAPI web endpoints.
- [`requirements.txt`](requirements.txt): Pinned dependencies for the environment.

---

## Live Web App & Shareable URL 🌐

You can access and share the live interactive application online directly via **GitHub Pages**:

👉 **[https://rajitha1881.github.io/healthy_relationships/](https://rajitha1881.github.io/healthy_relationships/)**

---

## 1. Setup Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Running the API Web Server

### Option A: Running with Python Locally
Start the application with:

```bash
python3 app.py
```
Or with Uvicorn:
```bash
uvicorn app:app --reload
```

The server runs at `http://127.0.0.1:8000`.

---

### Option B: Running with Docker 🐳

Build and run using Docker:

```bash
# 1. Build the Docker image
docker build -t healthy-relationships-app .

# 2. Run the container
docker run -p 8000:8000 --name healthy-app healthy-relationships-app
```

Or using **Docker Compose**:

```bash
docker compose up --build
```

Or pull the published image directly from **GitHub Packages (GHCR)**:

```bash
docker run -p 8000:8000 ghcr.io/rajitha1881/healthy_relationships:latest
```

The containerized app will be available at `http://localhost:8000`.

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

---

## 6. PR Checks & CI/CD Pipeline

A GitHub Actions workflow is configured in [`.github/workflows/pr-checks.yml`](.github/workflows/pr-checks.yml):

1. **Pull Request Checks**:
   - **Linting & Syntax Analysis**: Uses `ruff` and `flake8` to check for syntax errors, undefined variables, and code style.
   - **Matrix Testing**: Runs the complete test suite across Python `3.10`, `3.11`, `3.12`, and `3.13`.
   - **PR Quality Gate**: Verifies that all status checks have passed before allowing the merge.

2. **Main Branch Release Artifact & Docker Image Publishing**:
   - Once a PR is **merged into the `main` branch**, the pipeline automatically:
     - Generates and uploads a downloadable **Release Artifact** (`healthy-relationships-main-release`) containing code, test coverage HTML report, and build manifest.
     - Builds and pushes a production **Docker Container Image** to **GitHub Container Registry (GHCR)** tagged with `latest` and commit SHA (`ghcr.io/rajitha1881/healthy_relationships:latest`).
   - The container image appears under the **Packages** section on GitHub.

### Run PR Checks Locally:

Before creating a PR, you can run the exact same checks locally:

```bash
./scripts/run_checks.sh
```
