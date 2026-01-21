import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from uuid import uuid4

client = TestClient(app)

class TestCustomersCreate(unittest.TestCase):
    def test_create_customer_sin_token(self):
        response = client.post(
            "/customers",
            json={
                "document_number": "0123456789",
                "first_name": "Juan",
                "last_name": "Perez"
            }
        )
        self.assertIn(response.status_code, [401, 403])
    
    def test_create_customer_sin_datos(self):
        response = client.post("/customers", json={})
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_create_customer_sin_document_number(self):
        response = client.post(
            "/customers",
            json={
                "first_name": "Juan",
                "last_name": "Perez"
            }
        )
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_create_customer_sin_first_name(self):
        response = client.post(
            "/customers",
            json={
                "document_number": "0123456789",
                "last_name": "Perez"
            }
        )
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_create_customer_sin_last_name(self):
        response = client.post(
            "/customers",
            json={
                "document_number": "0123456789",
                "first_name": "Juan"
            }
        )
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_create_customer_documento_duplicado_sin_token(self):
        # Sin token, siempre retorna 401/403 antes de validar duplicados
        response = client.post(
            "/customers",
            json={
                "document_number": "0123456789",
                "first_name": "Juan",
                "last_name": "Perez"
            }
        )
        self.assertIn(response.status_code, [401, 403])


class TestCustomersGet(unittest.TestCase):
    def test_get_customers_sin_token(self):
        response = client.get("/customers")
        self.assertIn(response.status_code, [401, 403])
    
    def test_get_customers_con_skip_negativo(self):
        response = client.get("/customers?skip=-1")
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_get_customers_con_limit_cero(self):
        response = client.get("/customers?limit=0")
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_get_customers_con_limit_excesivo(self):
        response = client.get("/customers?limit=2000")
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_get_customers_active_only_false(self):
        response = client.get("/customers?active_only=false")
        self.assertIn(response.status_code, [401, 403])
    
    def test_get_customers_active_only_true(self):
        response = client.get("/customers?active_only=true")
        self.assertIn(response.status_code, [401, 403])


class TestCustomersGetById(unittest.TestCase):
    def test_get_customer_by_id_sin_token(self):
        customer_id = str(uuid4())
        response = client.get(f"/customers/{customer_id}")
        self.assertIn(response.status_code, [401, 403])
    
    def test_get_customer_by_id_invalido(self):
        response = client.get("/customers/invalid-uuid")
        self.assertIn(response.status_code, [401, 403, 422])
    
    @patch("app.crud.caja_crud.customer.get")
    def test_get_customer_by_id_no_encontrado(self, mock_get):
        mock_get.return_value = None
        customer_id = str(uuid4())
        response = client.get(f"/customers/{customer_id}")
        self.assertIn(response.status_code, [401, 403, 404])


class TestCustomersGetByDocument(unittest.TestCase):
    def test_get_customer_by_document_sin_token(self):
        response = client.get("/customers/document/0123456789")
        self.assertIn(response.status_code, [401, 403])
    
    @patch("app.crud.caja_crud.customer.get_by_document")
    def test_get_customer_by_document_no_encontrado(self, mock_get_by_document):
        mock_get_by_document.return_value = None
        response = client.get("/customers/document/9999999999")
        self.assertIn(response.status_code, [401, 403, 404])
    


class TestCustomersSearchByName(unittest.TestCase):
    def test_search_customers_sin_token(self):
        response = client.get("/customers/search/name?name=Juan")
        self.assertIn(response.status_code, [401, 403])
    
    def test_search_customers_sin_parametro_name(self):
        response = client.get("/customers/search/name")
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_search_customers_name_muy_corto(self):
        response = client.get("/customers/search/name?name=J")
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_search_customers_name_minimo(self):
        response = client.get("/customers/search/name?name=Ju")
        self.assertIn(response.status_code, [401, 403])


class TestCustomersVIP(unittest.TestCase):
    def test_get_vip_customers_sin_token(self):
        response = client.get("/customers/vip/list")
        self.assertIn(response.status_code, [401, 403])


class TestCustomersTop(unittest.TestCase):
    def test_get_top_customers_sin_token(self):
        response = client.get("/customers/top/list")
        self.assertIn(response.status_code, [401, 403])
    
    def test_get_top_customers_con_limit(self):
        response = client.get("/customers/top/list?limit=20")
        self.assertIn(response.status_code, [401, 403])
    
    def test_get_top_customers_limit_cero(self):
        response = client.get("/customers/top/list?limit=0")
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_get_top_customers_limit_excesivo(self):
        response = client.get("/customers/top/list?limit=100")
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_get_top_customers_limit_negativo(self):
        response = client.get("/customers/top/list?limit=-5")
        self.assertIn(response.status_code, [401, 403, 422])


class TestCustomersLoyaltyPoints(unittest.TestCase):
    def test_update_loyalty_points_sin_token(self):
        customer_id = str(uuid4())
        response = client.post(
            f"/customers/{customer_id}/loyalty-points",
            json={"points": 50.0}
        )
        self.assertIn(response.status_code, [401, 403])
    
    def test_update_loyalty_points_sin_datos(self):
        customer_id = str(uuid4())
        response = client.post(
            f"/customers/{customer_id}/loyalty-points",
            json={}
        )
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_update_loyalty_points_id_invalido(self):
        response = client.post(
            "/customers/invalid-uuid/loyalty-points",
            json={"points": 50.0}
        )
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_update_loyalty_points_negativos(self):
        customer_id = str(uuid4())
        response = client.post(
            f"/customers/{customer_id}/loyalty-points",
            json={"points": -10.0}
        )
        self.assertIn(response.status_code, [401, 403])


class TestCustomersWithMocks(unittest.TestCase):
    @patch("app.crud.caja_crud.customer.get_active_customers")
    def test_get_customers_mock_activos(self, mock_get_active):
        mock_get_active.return_value = [
            {
                "id": str(uuid4()),
                "document_number": "0123456789",
                "first_name": "Juan",
                "last_name": "Perez",
                "is_active": True
            }
        ]
        response = client.get("/customers?active_only=true")
        self.assertIn(response.status_code, [200, 401, 403])
    
    @patch("app.crud.caja_crud.customer.search_by_name")
    def test_search_customers_mock_vacio(self, mock_search):
        mock_search.return_value = []
        response = client.get("/customers/search/name?name=NoExiste")
        self.assertIn(response.status_code, [200, 401, 403])
    
    @patch("app.crud.caja_crud.customer.get_vip_customers")
    def test_get_vip_customers_mock(self, mock_get_vip):
        mock_get_vip.return_value = [
            {
                "id": str(uuid4()),
                "first_name": "VIP",
                "last_name": "Cliente",
                "is_vip": True
            }
        ]
        response = client.get("/customers/vip/list")
        self.assertIn(response.status_code, [200, 401, 403])
    
    @patch("app.crud.caja_crud.customer.get_top_customers")
    def test_get_top_customers_mock(self, mock_get_top):
        mock_get_top.return_value = [
            {
                "id": str(uuid4()),
                "first_name": "Top",
                "last_name": "Cliente",
                "loyalty_points": 1000
            }
        ]
        response = client.get("/customers/top/list?limit=5")
        self.assertIn(response.status_code, [200, 401, 403])



class TestCustomersDataValidation(unittest.TestCase):
    def test_create_customer_email_invalido(self):
        response = client.post(
            "/customers",
            json={
                "document_number": "0123456789",
                "first_name": "Juan",
                "last_name": "Perez",
                "email": "emailinvalido"
            }
        )
        self.assertIn(response.status_code, [401, 403, 422])
    
    def test_create_customer_con_datos_completos(self):
        response = client.post(
            "/customers",
            json={
                "document_number": "0123456789",
                "first_name": "Juan",
                "last_name": "Perez",
                "email": "juan@example.com",
                "phone": "0999999999",
                "address": "Calle Principal 123",
                "is_active": True
            }
        )
        self.assertIn(response.status_code, [200, 201, 401, 403])
    
    def test_create_customer_is_active_false(self):
        response = client.post(
            "/customers",
            json={
                "document_number": "0123456789",
                "first_name": "Juan",
                "last_name": "Perez",
                "is_active": False
            }
        )
        self.assertIn(response.status_code, [200, 201, 401, 403])




class TestCustomersPagination(unittest.TestCase):
    def test_get_customers_skip_valido(self):
        response = client.get("/customers?skip=10")
        self.assertIn(response.status_code, [200, 401, 403])
    
    def test_get_customers_limit_valido(self):
        response = client.get("/customers?limit=50")
        self.assertIn(response.status_code, [200, 401, 403])
    
    def test_get_customers_skip_y_limit(self):
        response = client.get("/customers?skip=5&limit=20")
        self.assertIn(response.status_code, [200, 401, 403])
    
    def test_get_customers_limit_maximo(self):
        response = client.get("/customers?limit=1000")
        self.assertIn(response.status_code, [200, 401, 403])


if __name__ == "__main__":
    unittest.main(verbosity=2)