from fastapi import FastAPI, HTTPException
from models import Product, Customer
from service import register_customer, register_product, buy, refund, customers


app = FastAPI()

@app.get("/clientes/{nome}")
def get_cliente(nome: str):
    if nome not in customers:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customers[nome]

@app.post("/clientes")
def criar_cliente(cliente: Customer):
    register_customer(cliente)
    return {"mensagem": "Cliente registrado com sucesso"}

@app.post("/produtos")
def criar_produto(produto: Product):
    register_product(produto)
    return {"mensagem": "Produto registrado com sucesso"}

@app.post("/comprar")
def comprar(cliente: str, produto: str, quantidade: int):
    try:
        buy(cliente, produto, quantidade)
        return {"mensagem": "Compra realizada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reembolso")
def reembolsar(cliente: str, produto: str, quantidade: int):
    try:
        refund(cliente, produto, quantidade)
        return {"mensagem": "Reembolso realizado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))