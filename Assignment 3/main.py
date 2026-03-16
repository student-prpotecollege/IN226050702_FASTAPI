from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Product Model
class Product(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool

# In-memory database
products = []
product_id_counter = 1


# GET all products
@app.get("/products")
def get_products():
    return products


# POST add product
@app.post("/products")
def add_product(product: Product):
    global product_id_counter

    # Check duplicate product name
    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_product = product.dict()
    new_product["id"] = product_id_counter

    products.append(new_product)
    product_id_counter += 1

    return {"message": "Product added", "product": new_product}


# PUT update product
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):

    for product in products:
        if product["id"] == product_id:
            product["name"] = updated_product.name
            product["price"] = updated_product.price
            product["category"] = updated_product.category
            product["in_stock"] = updated_product.in_stock

            return {"message": "Product updated", "product": product}

    raise HTTPException(status_code=404, detail="Product not found")


# DELETE product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": "Product deleted successfully"}

    raise HTTPException(status_code=404, detail="Product not found")
