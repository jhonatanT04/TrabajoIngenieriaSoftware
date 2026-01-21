import os
from uuid import uuid4

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db

init_db()
client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_register_and_login_and_product_flow():
    # registrar usuario admin para pruebas
    username = f"user_{uuid4().hex[:8]}"
    email = f"{username}@example.com"
    register_payload = {
        "username": username,
        "email": email,
        "password": "secret",
        "profile_name": "Administrador",
    }
    r = client.post("/auth/register", json=register_payload)
    assert r.status_code == 200
    data = r.json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # login para validar credenciales
    login_resp = client.post("/auth/login", json={"username": username, "password": "secret"})
    assert login_resp.status_code == 200

    # create product
    sku = f"SKU_{uuid4().hex[:8]}"
    p_payload = {
        "sku": sku,
        "name": "Producto 1",
        "cost_price": 5.0,
        "sale_price": 10.0,
        "stock_min": 0,
        "requires_lot_control": False,
        "requires_expiration_date": False,
        "is_active": True,
    }
    r = client.post("/products", json=p_payload, headers=headers)
    assert r.status_code == 200
    product = r.json()

    # list products
    r = client.get("/products", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # adjust inventory
    adj = {"product_id": product["id"], "new_quantity": 95, "reason": "venta manual"}
    r = client.post("/inventory/adjustment", json=adj, headers=headers)
    assert r.status_code == 200
