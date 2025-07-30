import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def setup_data():
    client.post("/clientes", json={"name": "Carlos", "balance": 5000})
    client.post("/produtos", json={"name": "Notebook", "price": 3000, "stock": 5})

def test_compra_valida(setup_data):
    resp = client.post("/comprar", params={"cliente": "Carlos", "produto": "Notebook", "quantidade": 1})
    assert resp.status_code == 200
    assert "Compra realizada" in resp.json()["mensagem"]

def test_compra_sem_saldo(setup_data):
    client.post("/clientes", json={"name": "João", "balance": 500})
    resp = client.post("/comprar", params={"cliente": "João", "produto": "Notebook", "quantidade": 1})
    assert resp.status_code == 400
    assert "Saldo insuficiente" in resp.json()["detail"]

def test_reembolso_valido(setup_data):
    client.post("/comprar", params={"cliente": "Carlos", "produto": "Notebook", "quantidade": 1})
    resp = client.post("/reembolso", params={"cliente": "Carlos", "produto": "Notebook", "quantidade": 1})
    assert resp.status_code == 200
    assert "Reembolso realizado" in resp.json()["mensagem"]

def test_reembolso_invalido(setup_data):
    resp = client.post("/reembolso", params={"cliente": "Carlos", "produto": "Notebook", "quantidade": 5})
    assert resp.status_code == 400
    assert "Produto não encontrado" in resp.json()["detail"]

def test_balance_atualizado_apos_compra_e_reembolso(setup_data):
    # Compra 1 notebook (3000), saldo inicial 5000
    resp = client.post("/comprar", params={"cliente": "Carlos", "produto": "Notebook", "quantidade": 1})
    assert resp.status_code == 200

    # Verifica saldo após compra
    resp = client.get(f"/clientes/{'Carlos'}")
    assert resp.status_code == 200
    assert resp.json()["balance"] == 2000  # 5000 - 3000

    # Reembolsa 1 notebook (3000)
    resp = client.post("/reembolso", params={"cliente": "Carlos", "produto": "Notebook", "quantidade": 1})
    assert resp.status_code == 200

    # Verifica saldo após reembolso
    resp = client.get(f"/clientes/{'Carlos'}")
    assert resp.status_code == 200
    assert resp.json()["balance"] == 5000  # 2000 + 3000