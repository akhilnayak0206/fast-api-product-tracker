
from fastapi import FastAPI

from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return "Hello, World!"
    
products = [
    Product(id=1, name="Product 1", price=10.0, description="Description 1", quantity=10),
    Product(id=2, name="Product 2", price=20.0, description="Description 2", quantity=20),
    Product(id=3, name="Product 3", price=30.0, description="Description 3", quantity=30)
]


@app.get("/products")
def get_all_products():
    return products


@app.get("/product/{id}")
def get_product(id: int):
    for product in products:
        if product.id == id:
            return product
    return "Product not found"

@app.post("/product")
def create_product(product: Product):
    products.append(product)
    return product


@app.put("/product/{id}")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product updated"
    return "Product not found"


@app.delete("/product/{id}")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            products.pop(i)
            return "Product deleted"
    return "Product not found"