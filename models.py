from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    stock: int

class Customer(BaseModel):
    name: str
    balance: float
    cart: dict[str, int] = {}