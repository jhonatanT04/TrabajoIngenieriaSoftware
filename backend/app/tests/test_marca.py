import unittest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestBrands(unittest.TestCase):

    def test_create_brand_sin_token(self):
        """Test: Crear marca sin autenticación"""
        response = client.post(
            "/brands",
            json={"name": "Samsung", "description": "Marca de electronicos"}
        )
        self.assertIn(response.status_code, [401, 403])

    def test_list_brands_sin_token(self):
        """Test: Listar marcas sin autenticación"""
        response = client.get("/brands")
        self.assertIn(response.status_code, [401, 403])

    def test_list_brands_con_paginacion_sin_token(self):
        """Test: Listar marcas con parámetros de paginación sin autenticación"""
        response = client.get("/brands?skip=0&limit=50")
        self.assertIn(response.status_code, [401, 403])

    def test_get_brand_sin_token(self):
        """Test: Obtener marca específica sin autenticación"""
        response = client.get(
            "/brands/123e4567-e89b-12d3-a456-426614174000"
        )
        self.assertIn(response.status_code, [401, 403])


if __name__ == "__main__":
    unittest.main()