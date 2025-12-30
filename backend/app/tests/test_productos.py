import unittest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestProducts(unittest.TestCase):

    def test_create_product_sin_token(self):
        """Test: Crear producto sin autenticación"""
        response = client.post(
            "/products",
            json={
                "name": "Laptop HP",
                "sku": "LAP-HP-001",
                "barcode": "7891234567890",
                "cost_price": 500.00,
                "sale_price": 750.00,
                "stock_min": 5,
                "stock_max": 50
            }
        )
        self.assertIn(response.status_code, [401, 403])

    def test_list_products_sin_token(self):
        """Test: Listar productos sin autenticación"""
        response = client.get("/products")
        self.assertIn(response.status_code, [401, 403])

    def test_list_products_con_paginacion_sin_token(self):
        """Test: Listar productos con parámetros sin autenticación"""
        response = client.get("/products?skip=0&limit=50&active_only=true")
        self.assertIn(response.status_code, [401, 403])

    def test_get_product_sin_token(self):
        """Test: Obtener producto por ID sin autenticación"""
        response = client.get(
            "/products/123e4567-e89b-12d3-a456-426614174000"
        )
        self.assertIn(response.status_code, [401, 403])

    def test_get_product_by_sku_sin_token(self):
        """Test: Obtener producto por SKU sin autenticación"""
        response = client.get("/products/sku/LAP-HP-001")
        self.assertIn(response.status_code, [401, 403])

    def test_get_product_by_barcode_sin_token(self):
        """Test: Obtener producto por código de barras sin autenticación"""
        response = client.get("/products/barcode/7891234567890")
        self.assertIn(response.status_code, [401, 403])

    def test_search_products_by_name_sin_token(self):
        """Test: Buscar productos por nombre sin autenticación"""
        response = client.get("/products/search/name?name=Laptop")
        self.assertIn(response.status_code, [401, 403])

    def test_get_products_by_category_sin_token(self):
        """Test: Obtener productos por categoría sin autenticación"""
        response = client.get(
            "/products/category/123e4567-e89b-12d3-a456-426614174000"
        )
        self.assertIn(response.status_code, [401, 403])

    def test_get_products_by_supplier_sin_token(self):
        """Test: Obtener productos por proveedor sin autenticación"""
        response = client.get(
            "/products/supplier/123e4567-e89b-12d3-a456-426614174000"
        )
        self.assertIn(response.status_code, [401, 403])

    def test_get_low_stock_products_sin_token(self):
        """Test: Obtener productos con stock bajo sin autenticación"""
        response = client.get("/products/low-stock/list")
        self.assertIn(response.status_code, [401, 403])

    def test_update_product_sin_token(self):
        """Test: Actualizar producto sin autenticación"""
        response = client.put(
            "/products/123e4567-e89b-12d3-a456-426614174000",
            json={
                "name": "Laptop HP Actualizada",
                "sku": "LAP-HP-001",
                "cost_price": 550.00,
                "sale_price": 800.00
            }
        )
        self.assertIn(response.status_code, [401, 403])

    def test_delete_product_sin_token(self):
        """Test: Desactivar producto sin autenticación"""
        response = client.delete(
            "/products/123e4567-e89b-12d3-a456-426614174000"
        )
        self.assertIn(response.status_code, [401, 403])


if __name__ == "__main__":
    unittest.main()