from models import Product, Customer

products: dict[str, Product] = {}
customers: dict[str, Customer] = {}

def register_product(product: Product):
    products[product.name] = product

def register_customer(customer: Customer):
    customers[customer.name] = customer

def buy(customer_name: str, product_name: str, quantity: int):
    customer = customers[customer_name]
    product = products[product_name]
    total_price = product.price * quantity

    if product.stock < quantity:
        raise ValueError("Estoque insuficiente")
    if customer.balance < total_price:
        raise ValueError("Saldo insuficiente")

    product.stock -= quantity
    customer.balance -= total_price
    customer.cart[product_name] = customer.cart.get(product_name, 0) + quantity

def refund(customer_name: str, product_name: str, quantity: int):
    customer = customers[customer_name]
    product = products[product_name]

    if product_name not in customer.cart or customer.cart[product_name] < quantity:
        raise ValueError("Produto não encontrado ou quantidade inválida para reembolso")

    product.stock += quantity
    customer.balance += product.price * quantity
    customer.cart[product_name] -= quantity
    if customer.cart[product_name] == 0:
        del customer.cart[product_name]