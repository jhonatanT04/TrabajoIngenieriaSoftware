import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from backend.main import app
from backend.app.database import init_db

init_db()
client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_register_and_login_and_product_flow():
    # register
    register_payload = {"username": "admin", "password": "secret", "full_name": "Admin User", "role": "admin"}
    r = client.post("/auth/register", json=register_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "admin"

    # token
    token_resp = client.post("/auth/token", data={"username": "admin", "password": "secret"})
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # create product
    p_payload = {"sku": "SKU1", "name": "Producto 1", "price_sale": 10.0, "stock": 100}
    r = client.post("/products/", json=p_payload)
    assert r.status_code == 200
    product = r.json()

    # list products
    r = client.get("/products/")
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # adjust inventory
    adj = {"product_id": product["id"], "quantity": -5, "reason": "venta manual"}
    r = client.post("/inventory/adjust", json=adj)
    assert r.status_code == 200
