import unittest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestSuppliers(unittest.TestCase):

    def test_create_supplier_sin_token(self):
        """Test: Crear proveedor sin autenticación"""
        response = client.post(
            "/suppliers",
            json={
                "business_name": "Distribuidora XYZ",
                "tax_id": "1234567890001",
                "contact_name": "Maria Garcia",
                "phone": "0999999999",
                "email": "contacto@xyz.com"
            }
        )
        self.assertIn(response.status_code, [401, 403])

    def test_list_suppliers_sin_token(self):
        """Test: Listar proveedores sin autenticación"""
        response = client.get("/suppliers")
        self.assertIn(response.status_code, [401, 403])

    def test_list_suppliers_con_parametros_sin_token(self):
        """Test: Listar proveedores con parámetro active_only sin autenticación"""
        response = client.get("/suppliers?active_only=true")
        self.assertIn(response.status_code, [401, 403])


class TestInventory(unittest.TestCase):

    def test_update_inventory_stock_sin_token(self):
        """Test: Actualizar stock de inventario sin autenticación"""
        response = client.post(
            "/inventory/update-stock",
            json={
                "product_id": "123e4567-e89b-12d3-a456-426614174000",
                "quantity": 100.0,
                "user_id": "123e4567-e89b-12d3-a456-426614174001"
            }
        )
        self.assertIn(response.status_code, [401, 403])

    def test_get_product_inventory_sin_token(self):
        """Test: Obtener inventario de un producto sin autenticación"""
        response = client.get(
            "/inventory/product/123e4567-e89b-12d3-a456-426614174000"
        )
        self.assertIn(response.status_code, [401, 403])

    


if __name__ == "__main__":
    unittest.main()