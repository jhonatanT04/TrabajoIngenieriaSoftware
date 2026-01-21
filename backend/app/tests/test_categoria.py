import unittest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestCategories(unittest.TestCase):

    def test_list_categories_sin_token(self):
        response = client.get("/categories")
        self.assertIn(response.status_code, [401, 403])

    def test_create_category_sin_token(self):
        response = client.post(
            "/categories",
            json={"name": "Electronica"}
        )
        self.assertIn(response.status_code, [401, 403])

    def test_root_categories_sin_token(self):
        response = client.get("/categories/root")
        self.assertIn(response.status_code, [401, 403])

    def test_subcategories_sin_token(self):
        response = client.get(
            "/categories/123e4567-e89b-12d3-a456-426614174000/subcategories"
        )
        self.assertIn(response.status_code, [401, 403])


if __name__ == "__main__":
    unittest.main()
