# ==============================================================================
# Unit and Integration Tests for Healthy Relationships API
# Built using Python's standard library - zero external dependencies required!
# ==============================================================================

import unittest
import threading
import json
import urllib.request
import urllib.error
from http.server import HTTPServer

from app import BuiltinRelationshipHandler, HAS_FASTAPI
from relationship_messages import MESSAGES


class TestBuiltinAPI(unittest.TestCase):
    """
    Tests the API using Python's standard library HTTP server and urllib.
    Runs on an ephemeral random OS port, avoiding port collisions.
    """

    @classmethod
    def setUpClass(cls):
        # Bind to port 0 to let the OS assign an available unused port
        cls.server = HTTPServer(("127.0.0.1", 0), BuiltinRelationshipHandler)
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        # Run the server in a background daemon thread
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        # Shut down the test server cleanly
        cls.server.shutdown()
        cls.server.server_close()

    def test_root_endpoint(self):
        """Test GET / returns 200 and online status."""
        with urllib.request.urlopen(f"{self.base_url}/") as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data["status"], "online")
            self.assertIn("endpoints", data)

    def test_categories_endpoint(self):
        """Test GET /categories returns all categories."""
        with urllib.request.urlopen(f"{self.base_url}/categories") as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertIn("categories", data)
            self.assertEqual(data["count"], len(MESSAGES))

    def test_get_random_message(self):
        """Test GET /message without parameters returns a random message."""
        with urllib.request.urlopen(f"{self.base_url}/message") as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data["category"], "random")
            self.assertIsInstance(data["message"], str)

    def test_get_message_by_query_growth(self):
        """Test GET /message?category=growth."""
        with urllib.request.urlopen(f"{self.base_url}/message?category=growth") as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data["category"], "growth")
            self.assertIn(data["message"], MESSAGES["growth"])

    def test_get_message_by_path_communication(self):
        """Test GET /message/communication."""
        with urllib.request.urlopen(f"{self.base_url}/message/communication") as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data["category"], "communication")
            self.assertIn(data["message"], MESSAGES["communication"])

    def test_post_message_payload(self):
        """Test POST /message with JSON payload."""
        payload_bytes = json.dumps({"category": "boundaries"}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/message",
            data=payload_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data["category"], "boundaries")
            self.assertIn(data["message"], MESSAGES["boundaries"])

    def test_invalid_category_returns_404(self):
        """Test requesting an invalid category returns HTTP 404."""
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(f"{self.base_url}/message/invalid_category")
        self.assertEqual(ctx.exception.code, 404)
        error_data = json.loads(ctx.exception.read().decode())
        self.assertIn("Unknown category", error_data["detail"])


# ==============================================================================
# Optional: FastAPI TestClient Tests (Only runs if FastAPI is installed)
# ==============================================================================
if HAS_FASTAPI:
    try:
        from fastapi.testclient import TestClient
        from app import app

        class TestFastAPI(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                cls.client = TestClient(app)

            def test_fastapi_root(self):
                res = self.client.get("/")
                self.assertEqual(res.status_code, 200)

            def test_fastapi_message(self):
                res = self.client.get("/message?category=growth")
                self.assertEqual(res.status_code, 200)
                self.assertEqual(res.json()["category"], "growth")
    except ImportError:
        pass


if __name__ == "__main__":
    unittest.main()
