# Operations Runbook: Healthy Relationships API & Web App

**Service Name**: Healthy Relationships Platform  
**Owner / Maintainer**: Rajitha1881  
**Repository**: [https://github.com/Rajitha1881/healthy_relationships](https://github.com/Rajitha1881/healthy_relationships)  
**Production API URL**: `https://healthy-relationships.onrender.com`  
**Swagger UI Docs**: `https://healthy-relationships.onrender.com/docs`  
**Public Web App (GitHub Pages)**: `https://rajitha1881.github.io/healthy_relationships/`  
**Container Registry**: `ghcr.io/rajitha1881/healthy_relationships:latest`

---

## Table of Contents

1. [Architecture & System Overview](#1-architecture--system-overview)
2. [Prerequisites & Environment Setup](#2-prerequisites--environment-setup)
3. [Local Development Playbook](#3-local-development-playbook)
4. [Docker & Container Operations](#4-docker--container-operations)
5. [CI/CD Pipeline & Release Workflow](#5-cicd-pipeline--release-workflow)
6. [Cloud Deployment Procedures](#6-cloud-deployment-procedures)
7. [API Endpoints Reference (v1 & v2)](#7-api-endpoints-reference-v1--v2)
8. [Monitoring & Healthchecks](#8-monitoring--healthchecks)
9. [Incident Response & Troubleshooting](#9-incident-response--troubleshooting)
10. [Rollback Procedures](#10-rollback-procedures)

---

## 1. Architecture & System Overview

The application is structured into three integrated components:

```
                      +-----------------------------+
                      | healthy_relationships Repo  |
                      +--------------+--------------+
                                     |
             +-----------------------+-----------------------+
             |                       |                       |
             v                       v                       v
     [ GitHub Pages ]        [ GitHub Packages ]     [ Render Cloud ]
   Static Web Frontend        Container Registry      Live Backend API
https://rajitha1881.github.io     (ghcr.io)       https://healthy-relationships
   /healthy_relationships                           .onrender.com
             |                       |                       |
      Pure Client-side        Docker Image             FastAPI + Uvicorn
      JavaScript & HTML       v1 / v2 / latest        REST Endpoints & Docs
```

### Core Technologies
- **Language**: Python 3.10+ (Recommended: Python 3.12)
- **Web Framework**: FastAPI with Pydantic v2 schemas
- **ASGI Server**: Uvicorn
- **Fallback Server**: Python Standard Library `http.server` (zero dependencies required)
- **Containerization**: Docker (multi-stage non-root user `appuser:1000`)
- **CI/CD**: GitHub Actions (Linting, Multi-Python Test Matrix 3.10-3.13, GHCR publishing, Artifact upload)
- **PaaS Host**: Render (Free Tier Web Service)

---

## 2. Prerequisites & Environment Setup

Before working on the application, ensure you have:

- **Python**: `python3 --version` $\ge$ 3.10
- **Git**: `git --version`
- **Docker Desktop** (optional for local container testing): `docker --version`
- **GitHub CLI** (optional for PRs): `gh --version`

---

## 3. Local Development Playbook

### 3.1 Quick Start (Zero Dependencies)
You can run the application directly using your system Python without creating a virtual environment:

```bash
python3 app.py
```
*The app automatically detects that FastAPI is not installed globally and launches the built-in HTTP server on `http://127.0.0.1:8000`.*

### 3.2 Full Development Environment (FastAPI + Swagger Docs)
To enable the full FastAPI framework, interactive `/docs`, and automatic reloading:

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Start local server
python3 app.py
```

- Open in browser: `http://localhost:8000`
- Open Swagger UI: `http://localhost:8000/docs`

### 3.3 Running Unit & Integration Tests
Before committing changes, execute the local check suite:

```bash
# Run local all-in-one check script
./scripts/run_checks.sh

# Or run unittest directly:
python3 -m unittest discover -v
```

---

## 4. Docker & Container Operations

### 4.1 Running with Docker Compose (Recommended)
```bash
# Build and start container in background
docker compose up -d --build

# View real-time container logs
docker compose logs -f

# Stop and clean up containers
docker compose down
```

### 4.2 Running with Pure Docker CLI
```bash
# Build local image
docker build -t healthy-relationships-app .

# Run container with port forwarding
docker run -d -p 8000:8000 --name healthy-app healthy-relationships-app

# Pull and run directly from GitHub Container Registry
docker run -d -p 8000:8000 --name healthy-app ghcr.io/rajitha1881/healthy_relationships:latest
```

### 4.3 Container Lifecycle Management
| Action | Command |
|---|---|
| Check running status | `docker ps` |
| View container logs | `docker logs -f healthy-app` |
| Stop container | `docker stop healthy-app` |
| Restart container | `docker start healthy-app` |
| Force remove container | `docker rm -f healthy-app` |

---

## 5. CI/CD Pipeline & Release Workflow

The automated pipeline is defined in [`.github/workflows/pr-checks.yml`](.github/workflows/pr-checks.yml).

### 5.1 Pipeline Stages

```
   [ Pull Request Open / Updated ]
                  │
      ├── 1. Code Linting (Ruff syntax check + Flake8 complexity)
      ├── 2. Test Matrix (Python 3.10, 3.11, 3.12, 3.13 in parallel)
      ├── 3. PR Quality Gate (Enforces 100% pass rate)
      └── 4. Docker Build Verification (Dry run without pushing)
                  │
                  ▼
         [ Merge into 'main' ]
                  │
      ├── 5. Package Artifact (`healthy-relationships-main-release.zip`)
      ├── 6. Build & Publish Docker Image (`ghcr.io/...:latest`)
      └── 7. Deploy Static Site to GitHub Pages
```

### 5.2 Branching & Pull Request Standard
1. Create a task branch:
   ```bash
   git checkout -b task/feature-name
   ```
2. Verify all checks pass locally:
   ```bash
   ./scripts/run_checks.sh
   ```
3. Commit and push:
   ```bash
   git add .
   git commit -m "feat: description of change"
   git push origin task/feature-name
   ```
4. Open PR targeting `main`:
   ```bash
   gh pr create --base main --head task/feature-name --title "feat: description"
   ```
5. Merge once all automated checks pass.

---

## 6. Cloud Deployment Procedures

### 6.1 Backend API Deployment (Render Cloud)
The backend REST API is hosted on Render using the [`Dockerfile`](Dockerfile).

- **Deployment Mode**: Automatic Webhook on push to `main`.
- **Healthcheck Path**: `/categories`
- **Dashboard**: [https://dashboard.render.com](https://dashboard.render.com)

#### Manual Redeployment Trigger:
1. Go to the Render Dashboard.
2. Select `healthy-relationships`.
3. Click **"Manual Deploy"** $\rightarrow$ **"Deploy latest commit"**.

### 6.2 Frontend Web App Deployment (GitHub Pages)
The interactive web app is deployed directly through GitHub Actions:
- **Build Script**: [`scripts/build_static_site.py`](scripts/build_static_site.py)
- **Destination**: GitHub Pages environment (`public/` directory).
- **URL**: `https://rajitha1881.github.io/healthy_relationships/`

---

## 7. API Endpoints Reference (v1 & v2)

### Version 1 (Core / Legacy)
| Method | Route | Description | Query Parameters |
|---|---|---|---|
| `GET` | `/categories` | List all category strings | None |
| `GET` | `/message` | Return random or categorized message | `?category=growth` |
| `GET` | `/message/{category}`| Path parameter lookup | None |
| `POST` | `/message` | JSON body lookup (`{"category": "..."}`) | None |

### Version 2 (Enhanced with Challenges & Analytics)
| Method | Route | Description | Sample Output |
|---|---|---|---|
| `GET` | `/api/v2/message` | Rich message with actionable challenge & tags | `{ "id": "...", "actionable_challenge": "...", "tags": [...] }` |
| `GET` | `/api/v2/daily-challenge` | Dedicated daily relationship exercise | `{ "daily_challenge": "...", "difficulty": "...", "duration": 10 }` |
| `GET` | `/api/v2/categories` | Categories with message count and tags | `{ "categories": [{ "category": "growth", "total_messages": 3 }] }` |

---

## 8. Monitoring & Healthchecks

### 8.1 Healthcheck URLs
- **Production API Health**:
  ```bash
  curl -i https://healthy-relationships.onrender.com/categories
  ```
  Expected status: `HTTP/2 200`
- **Local Healthcheck**:
  ```bash
  curl -i http://localhost:8000/categories
  ```

### 8.2 Container Health Verification
```bash
docker inspect --format='{{json .State.Health}}' healthy-app
```
Expected output contains `"Status": "healthy"`.

### 8.3 Viewing Production Logs
1. **Render Dashboard**: Navigate to `healthy-relationships` $\rightarrow$ **Logs**.
2. **Terminal Stream**:
   ```bash
   # If running locally or via Docker:
   docker logs -f healthy-app
   ```

---

## 9. Incident Response & Troubleshooting

### Incident 1: `ERR_CONNECTION_REFUSED` on `localhost:8000`
- **Symptom**: Browser or `curl` reports connection refused.
- **Root Cause**: The local server is not running or crashed.
- **Remediation**:
  1. Check if the process is running: `lsof -i :8000`
  2. If clear, restart the server: `python3 app.py`

### Incident 2: `502 Bad Gateway` or `Not Found` on Render
- **Symptom**: `https://healthy-relationships.onrender.com` returns 502 or 404.
- **Root Cause**: 
  - On the Free tier, Render puts containers to sleep after 15 minutes of inactivity. The first request will take 30–50 seconds to spin up.
  - If it returns 404 with `x-render-routing: no-server`, verify the exact service URL in the Render dashboard.
- **Remediation**:
  1. Wait 45 seconds and reload.
  2. Inspect the Render Deploy Logs for startup errors.

### Incident 3: `ModuleNotFoundError: No module named 'fastapi'`
- **Symptom**: Error thrown when running tests or starting server.
- **Root Cause**: Command executed against system Python without activating virtual environment.
- **Remediation**:
  1. Use the virtual environment binary explicitly:
     ```bash
     .venv/bin/python app.py
     ```
  2. Or activate the venv: `source .venv/bin/activate`

### Incident 4: CI/CD Pipeline Fails on Pull Request
- **Symptom**: Red ❌ on GitHub PR check.
- **Root Cause**: Linter error (`ruff`), formatting issue, or failing unit test.
- **Remediation**:
  1. Run the local check script to isolate the issue:
     ```bash
     ./scripts/run_checks.sh
     ```
  2. Fix any syntax or test failures, commit, and push back to the branch.

---

## 10. Rollback Procedures

### 10.1 Instant Git Rollback (Main Branch)
If a bad commit was merged to `main`:

```bash
# 1. Switch to main and pull latest
git checkout main
git pull origin main

# 2. Revert the problematic commit
git revert <COMMIT_HASH> -m 1

# 3. Push revert to main
git push origin main
```
*Pushing to `main` will automatically trigger the CI/CD pipeline and redeploy the previous stable state to Render and GitHub Pages.*

### 10.2 Render Deployment Rollback
1. Open [https://dashboard.render.com](https://dashboard.render.com).
2. Click **`healthy-relationships`** $\rightarrow$ **Events**.
3. Locate the previous successful deploy $\rightarrow$ click the three dots (`...`) $\rightarrow$ select **"Rollback to this deploy"**.

