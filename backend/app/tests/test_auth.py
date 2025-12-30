import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


class TestAuthLogin(unittest.TestCase):

    def test_login_sin_datos(self):
        response = client.post("/auth/login", json={})
        self.assertEqual(response.status_code, 422)

    def test_login_invalido(self):
        response = client.post(
            "/auth/login",
            json={"username": "fake", "password": "fake"}
        )
        self.assertEqual(response.status_code, 401)


class TestAuthRegister(unittest.TestCase):

    @patch("crud.users_crud.user.get_by_username")
    def test_register_usuario_existente(self, mock_get_user):
        mock_get_user.return_value = True

        response = client.post(
            "/auth/register",
            json={
                "username": "admin",
                "email": "admin@minimercado.com",
                "password": "123"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_register_sin_datos(self):
        response = client.post("/auth/register", json={})
        self.assertEqual(response.status_code, 422)


class TestAuthProtected(unittest.TestCase):

    def test_me_sin_token(self):
        response = client.get("/auth/me")
        self.assertIn(response.status_code, [401, 403])

    def test_refresh_sin_token(self):
        response = client.post("/auth/refresh")
        self.assertIn(response.status_code, [401, 403])

    def test_change_password_sin_token(self):
        response = client.put(
            "/auth/change-password",
            json={
                "current_password": "123",
                "new_password": "12345678"
            }
        )
        self.assertIn(response.status_code, [401, 403])


if __name__ == "__main__":
    unittest.main()
