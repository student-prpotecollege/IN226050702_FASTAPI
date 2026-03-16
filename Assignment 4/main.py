from fastapi import FastAPI, HTTPException

app = FastAPI()

# Sample product database
products = {
    1: {"name": "Wireless Mouse", "price": 499},
    2: {"name": "Notebook", "price": 99},
    3: {"name": "Pen", "price": 10}
}

# Cart storage
cart = {}


# Q1 — Add item to cart
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[product_id]
    subtotal = product["price"] * quantity

    cart[product_id] = {
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": subtotal
    }

    return {
        "message": "Added to cart",
        "cart_item": {
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "subtotal": subtotal
        }
    }


# Q2 — View cart
@app.get("/cart/view")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    total = sum(item["subtotal"] for item in cart.values())

    return {
        "cart_items": cart,
        "total_price": total
    }


# Q3 — Error handling example
@app.get("/product/{product_id}")
def get_product(product_id: int):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    return products[product_id]


# Q4 — Update cart quantity
@app.put("/cart/update")
def update_cart(product_id: int, quantity: int):

    if product_id not in cart:
        raise HTTPException(status_code=404, detail="Product not in cart")

    product = products[product_id]

    cart[product_id]["quantity"] = quantity
    cart[product_id]["subtotal"] = quantity * product["price"]

    return {
        "message": "Cart updated successfully",
        "cart_item": {
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "subtotal": cart[product_id]["subtotal"]
        }
    }


# Q5 — Remove item from cart
@app.delete("/cart/remove")
def remove_from_cart(product_id: int):

    if product_id not in cart:
        raise HTTPException(status_code=404, detail="Product not in cart")

    removed_item = cart.pop(product_id)

    return {
        "message": "Item removed from cart",
        "removed_item": removed_item
    }


# Q6 — Checkout
@app.post("/cart/checkout")
def checkout():

    if not cart:
        return {"message": "Cart is empty"}

    total = sum(item["subtotal"] for item in cart.values())

    cart.clear()

    return {
        "message": "Checkout successful",
        "total_paid": total
    }
