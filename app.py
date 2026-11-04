# ==============================================================================
# Healthy Relationships API & Web App Server
# Supports both FastAPI (with Swagger /docs) and Python's built-in HTTP server
# (zero external dependencies required!).
# ==============================================================================

import json
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, List

# Core message functions from relationship_messages.py
from relationship_messages import (
    get_relationship_message,
    get_categories,
    get_relationship_message_v2,
    get_daily_challenge,
    MESSAGES,
    CHALLENGES,
    TAGS,
)

# Check if FastAPI is installed in the active environment
try:
    from fastapi import FastAPI, HTTPException, Query, Request, APIRouter
    from fastapi.responses import HTMLResponse, JSONResponse
    from pydantic import BaseModel, Field
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


# ==============================================================================
# Interactive HTML Web Interface (Rendered when opened in a Web Browser)
# ==============================================================================
HTML_UI = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Healthy Relationships App</title>
  <style>
    :root {
      --primary: #4f46e5;
      --primary-hover: #4338ca;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #1e293b;
      --muted: #64748b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    body { background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
    .card { background: var(--card-bg); max-width: 620px; width: 100%; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04); padding: 32px; text-align: center; border: 1px solid #e2e8f0; }
    h1 { font-size: 1.75rem; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
    p.subtitle { color: var(--muted); font-size: 0.95rem; margin-bottom: 24px; }
    .message-box { background: #f1f5f9; border-radius: 12px; padding: 24px; margin-bottom: 24px; min-height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; border-left: 4px solid var(--primary); transition: all 0.2s ease; }
    .category-badge { display: inline-block; background: var(--primary); color: white; padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px; }
    .message-text { font-size: 1.15rem; font-weight: 500; line-height: 1.6; color: #1e293b; }
    .btn-group { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 24px; }
    button { background: #ffffff; color: #334155; border: 1px solid #cbd5e1; padding: 10px 16px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.15s ease; }
    button:hover { background: #f8fafc; border-color: var(--primary); color: var(--primary); transform: translateY(-1px); }
    button.btn-primary { background: var(--primary); color: white; border-color: var(--primary); }
    button.btn-primary:hover { background: var(--primary-hover); color: white; }
    .api-links { margin-top: 20px; font-size: 0.85rem; color: var(--muted); border-top: 1px solid #e2e8f0; padding-top: 16px; }
    .api-links a { color: var(--primary); text-decoration: none; font-weight: 500; margin: 0 6px; }
    .api-links a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Healthy Relationships</h1>
    <p class="subtitle">Daily guidance, healthy communication tips, and relationship affirmations</p>

    <div class="message-box" id="box">
      <span class="category-badge" id="categoryBadge">Growth</span>
      <p class="message-text" id="messageText">Celebrate each other's personal growth, even when it brings new changes.</p>
    </div>

    <div class="btn-group">
      <button class="btn-primary" onclick="fetchMessage()">🎲 Any Random</button>
      <button onclick="fetchMessage('growth')">🌱 Growth</button>
      <button onclick="fetchMessage('communication')">💬 Communication</button>
      <button onclick="fetchMessage('appreciation')">❤️ Appreciation</button>
      <button onclick="fetchMessage('boundaries')">🛡️ Boundaries</button>
      <button onclick="fetchMessage('conflict_resolution')">🤝 Conflict Resolution</button>
    </div>

    <div class="api-links">
      <span>Direct API endpoints:</span>
      <a href="/message?category=growth" target="_blank">/message?category=growth</a> |
      <a href="/categories" target="_blank">/categories</a> |
      <a href="/message" target="_blank">/message (raw JSON)</a>
    </div>
  </div>

  <script>
    async function fetchMessage(category = '') {
      const url = category ? `/message?category=${encodeURIComponent(category)}` : '/message';
      try {
        const response = await fetch(url);
        const data = await response.json();
        document.getElementById('categoryBadge').innerText = data.category.replace('_', ' ');
        document.getElementById('messageText').innerText = data.message;
      } catch (err) {
        console.error('Error fetching message:', err);
      }
    }
  </script>
</body>
</html>
"""


# ==============================================================================
# FastAPI Application Definition (When FastAPI is installed)
# ==============================================================================
if HAS_FASTAPI:
    app = FastAPI(
        title="Healthy Relationships API",
        description="A multi-version API providing healthy relationship advice, tips, affirmations, and actionable challenges.",
        version="2.0.0",
    )

    # --------------------------------------------------------------------------
    # Schemas: Version 1 (Basic / Flat Format)
    # --------------------------------------------------------------------------
    class MessageResponse(BaseModel):
        category: str = Field(..., description="The category of the relationship message.")
        message: str = Field(..., description="The advice or affirmation.")

    class MessageRequest(BaseModel):
        category: Optional[str] = Field(default=None, description="Optional category filter.")

    class CategoriesResponse(BaseModel):
        categories: List[str]
        count: int

    # --------------------------------------------------------------------------
    # Schemas: Version 2 (Enhanced with Challenges & Metadata)
    # --------------------------------------------------------------------------
    class MessageMetadata(BaseModel):
        char_count: int = Field(..., description="Total characters in the message.")
        word_count: int = Field(..., description="Total words in the message.")
        estimated_read_seconds: int = Field(..., description="Estimated reading duration.")
        community_rating: float = Field(..., description="Average rating for this message.")

    class MessageResponseV2(BaseModel):
        id: str = Field(..., description="Unique message ID.")
        version: str = Field("2.0", description="API schema version.")
        category: str = Field(..., description="The message category.")
        message: str = Field(..., description="The affirmation or relationship guidance.")
        actionable_challenge: str = Field(..., description="A real-world actionable challenge to practice today.")
        tags: List[str] = Field(..., description="Psychological and relationship topic tags.")
        metadata: MessageMetadata = Field(..., description="Analytical message metadata.")

    class DailyChallengeResponse(BaseModel):
        version: str = Field("2.0", description="API schema version.")
        category: str = Field(..., description="Challenge category.")
        daily_challenge: str = Field(..., description="The challenge to practice today.")
        difficulty: str = Field(..., description="Challenge intensity (e.g. Gentle & Easy, Deep Connection).")
        recommended_duration_minutes: int = Field(..., description="Suggested time to spend on challenge.")

    # --------------------------------------------------------------------------
    # Root & General Endpoints
    # --------------------------------------------------------------------------
    @app.get("/", summary="Root Endpoint")
    def root(request: Request):
        # If opened in a browser (Accept: text/html), serve the interactive web app!
        accept_header = request.headers.get("accept", "")
        if "text/html" in accept_header:
            return HTMLResponse(content=HTML_UI)

        return {
            "app": "Healthy Relationships API",
            "status": "online",
            "documentation": "/docs",
            "versions": {
                "v1": {
                    "description": "Standard basic message API",
                    "endpoints": ["GET /api/v1/message", "GET /api/v1/categories"]
                },
                "v2": {
                    "description": "Enhanced API with actionable daily challenges, tags, and analytics",
                    "endpoints": ["GET /api/v2/message", "GET /api/v2/daily-challenge", "GET /api/v2/categories"]
                }
            },
        }

    @app.get("/categories", response_model=CategoriesResponse, summary="List Categories (Default)", tags=["General"])
    def list_categories():
        cats = get_categories()
        return {"categories": cats, "count": len(cats)}

    @app.get("/message", response_model=MessageResponse, summary="Get Message (Default / Backward Compatible)", tags=["General"])
    def get_message_by_query(category: Optional[str] = Query(default=None)):
        try:
            msg = get_relationship_message(category)
            cat_name = category.strip().lower() if category else "random"
            return {"category": cat_name, "message": msg}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.get("/message/{category}", response_model=MessageResponse, summary="Get Message by Path", tags=["General"])
    def get_message_by_path(category: str):
        try:
            msg = get_relationship_message(category)
            return {"category": category.strip().lower(), "message": msg}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.post("/message", response_model=MessageResponse, summary="Get Message via POST", tags=["General"])
    def post_message_request(payload: MessageRequest):
        try:
            msg = get_relationship_message(payload.category)
            cat_name = payload.category.strip().lower() if payload.category else "random"
            return {"category": cat_name, "message": msg}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    # --------------------------------------------------------------------------
    # Version 1 Router (/api/v1)
    # --------------------------------------------------------------------------
    v1_router = APIRouter(prefix="/api/v1", tags=["Version 1 - Basic"])

    @v1_router.get("/message", response_model=MessageResponse, summary="Get Message (v1)")
    def v1_get_message(category: Optional[str] = Query(default=None)):
        """Returns standard v1 message string and category."""
        try:
            msg = get_relationship_message(category)
            cat_name = category.strip().lower() if category else "random"
            return {"category": cat_name, "message": msg}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @v1_router.get("/categories", response_model=CategoriesResponse, summary="List Categories (v1)")
    def v1_list_categories():
        cats = get_categories()
        return {"categories": cats, "count": len(cats)}

    app.include_router(v1_router)

    # --------------------------------------------------------------------------
    # Version 2 Router (/api/v2) - New Features!
    # --------------------------------------------------------------------------
    v2_router = APIRouter(prefix="/api/v2", tags=["Version 2 - Enhanced with Challenges"])

    @v2_router.get("/message", response_model=MessageResponseV2, summary="Get Rich Message with Challenge (v2)")
    def v2_get_message(category: Optional[str] = Query(default=None, description="Optional category (growth, communication, etc.)")):
        """
        **V2 Endpoint**: Returns a rich relationship object containing:
        - Unique ID
        - Advice message
        - **Actionable real-world challenge to practice today**
        - Psychological tags
        - Analytical metadata (char count, read time, rating)
        """
        try:
            return get_relationship_message_v2(category)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @v2_router.get("/daily-challenge", response_model=DailyChallengeResponse, summary="Get Daily Actionable Challenge (v2)")
    def v2_get_daily_challenge(category: Optional[str] = Query(default=None)):
        """
        **V2 Unique Endpoint**: Generates an actionable daily exercise designed to improve communication, appreciation, or boundaries.
        """
        try:
            return get_daily_challenge(category)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @v2_router.get("/categories", summary="List Categories with Metadata (v2)")
    def v2_list_categories():
        """
        **V2 Endpoint**: Returns all categories enriched with item counts and tags.
        """
        cats = []
        for key in MESSAGES.keys():
            cats.append({
                "category": key,
                "total_messages": len(MESSAGES[key]),
                "total_challenges": len(CHALLENGES.get(key, [])),
                "tags": TAGS.get(key, []),
            })
        return {"version": "2.0", "total_categories": len(cats), "categories": cats}

    app.include_router(v2_router)


# ==============================================================================
# Built-in Fallback Handler (Zero Dependencies - standard library only)
# ==============================================================================
class BuiltinRelationshipHandler(BaseHTTPRequestHandler):
    """Handles HTTP requests using Python's standard library (no pip packages needed)."""

    def _send_json(self, status_code: int, data: dict):
        response_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response_bytes)

    def _send_html(self, status_code: int, html_str: str):
        response_bytes = html_str.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_HEAD(self):
        # Allow HEAD requests (used by some browsers and health-checkers)
        self.do_GET()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query_params = parse_qs(parsed.query)

        # 1. Root: GET /
        if path == "" or path == "/":
            # If opened in a web browser, return the interactive HTML page
            accept_header = self.headers.get("Accept", "")
            if "text/html" in accept_header:
                self._send_html(200, HTML_UI)
                return

            # Otherwise return JSON API directory
            self._send_json(200, {
                "app": "Healthy Relationships API (Standard Library Server)",
                "status": "online",
                "endpoints": {
                    "GET /categories": "List all categories",
                    "GET /message": "Get message (supports ?category=...)",
                    "GET /message/<category>": "Get message by category path",
                    "POST /message": "Get message with JSON body",
                },
            })
            return

        # 2. Categories: GET /categories or /api/v1/categories
        if path in ("/categories", "/api/v1/categories"):
            cats = get_categories()
            self._send_json(200, {"categories": cats, "count": len(cats)})
            return

        # 3. Message by query: GET /message or /api/v1/message
        if path in ("/message", "/api/v1/message"):
            category = query_params.get("category", [None])[0]
            try:
                msg = get_relationship_message(category)
                cat_name = category.strip().lower() if category else "random"
                self._send_json(200, {"category": cat_name, "message": msg})
            except ValueError as e:
                self._send_json(404, {"detail": str(e)})
            return

        # 4. V2 Message: GET /api/v2/message
        if path == "/api/v2/message":
            category = query_params.get("category", [None])[0]
            try:
                data = get_relationship_message_v2(category)
                self._send_json(200, data)
            except ValueError as e:
                self._send_json(404, {"detail": str(e)})
            return

        # 5. V2 Daily Challenge: GET /api/v2/daily-challenge
        if path == "/api/v2/daily-challenge":
            category = query_params.get("category", [None])[0]
            try:
                data = get_daily_challenge(category)
                self._send_json(200, data)
            except ValueError as e:
                self._send_json(404, {"detail": str(e)})
            return

        # 6. V2 Categories: GET /api/v2/categories
        if path == "/api/v2/categories":
            cats = []
            for key in MESSAGES.keys():
                cats.append({
                    "category": key,
                    "total_messages": len(MESSAGES[key]),
                    "total_challenges": len(CHALLENGES.get(key, [])),
                    "tags": TAGS.get(key, []),
                })
            self._send_json(200, {"version": "2.0", "total_categories": len(cats), "categories": cats})
            return

        # 7. Message by path: GET /message/<category>
        parts = path.split("/")
        if len(parts) == 3 and parts[1] == "message":
            category = parts[2]
            try:
                msg = get_relationship_message(category)
                self._send_json(200, {"category": category.strip().lower(), "message": msg})
            except ValueError as e:
                self._send_json(404, {"detail": str(e)})
            return

        # Unknown route: 404
        self._send_json(404, {"detail": f"Route '{self.path}' not found."})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/message":
            content_length = int(self.headers.get("Content-Length", 0))
            category = None
            if content_length > 0:
                try:
                    body = json.loads(self.rfile.read(content_length).decode("utf-8"))
                    category = body.get("category")
                except json.JSONDecodeError:
                    self._send_json(400, {"detail": "Invalid JSON payload."})
                    return

            try:
                msg = get_relationship_message(category)
                cat_name = category.strip().lower() if category else "random"
                self._send_json(200, {"category": cat_name, "message": msg})
            except ValueError as e:
                self._send_json(404, {"detail": str(e)})
            return

        self._send_json(404, {"detail": f"Route '{self.path}' not found."})

    def log_message(self, format, *args):
        # Clean terminal logging
        print(f"[HTTP Server] {self.address_string()} - {format % args}")


# ==============================================================================
# Server Startup Entry Point
# ==============================================================================
def start_server(host: Optional[str] = None, port: Optional[int] = None):
    import os
    # Read host and port from environment variables, defaulting to 0.0.0.0:8000
    # (0.0.0.0 allows connections from both localhost and Docker container networks)
    resolved_host = host or os.getenv("HOST", "0.0.0.0")
    resolved_port = port or int(os.getenv("PORT", 8000))
    reload_enabled = os.getenv("RELOAD", "false").lower() == "true"

    if HAS_FASTAPI:
        import uvicorn
        print("Starting FastAPI server with Uvicorn...")
        print(f"Web App & API URL: http://{resolved_host}:{resolved_port}")
        print(f"Interactive Swagger Docs: http://{resolved_host}:{resolved_port}/docs\n")
        uvicorn.run("app:app", host=resolved_host, port=resolved_port, reload=reload_enabled)
    else:
        print(f"FastAPI not detected in current environment.")
        print(f"Starting built-in Python HTTP server at http://{resolved_host}:{resolved_port}")
        print("Note: To run with FastAPI and interactive /docs, run: .venv/bin/python app.py\n")
        server = HTTPServer((resolved_host, resolved_port), BuiltinRelationshipHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    start_server()
