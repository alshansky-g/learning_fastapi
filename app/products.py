from fastapi import FastAPI

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99,
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99,
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99,
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99,
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99,
}

sample_products = [
    sample_product_1,
    sample_product_2,
    sample_product_3,
    sample_product_4,
    sample_product_5,
]

app = FastAPI()


@app.get("/product/{product_id}")
def get_product_by_id(product_id: int):
    for sample in sample_products:
        if sample["product_id"] == product_id:
            return sample
    return {"message": f"Товар с id={product_id} не найден."}


@app.get("/products/search")
def search_products(
    keyword: str, category: str | None = None, limit: int | None = None
):
    filtered_products = (
        product
        for product in sample_products
        if keyword.lower() in product["name"].lower()
    )
    if category is not None:
        filtered_products = (
            product
            for product in filtered_products
            if category.lower() in product["category"].lower()
        )
    filtered_products = list(filtered_products)
    if limit is not None:
        filtered_products = filtered_products[:limit]
    return filtered_products
