from sanic import Blueprint, json

products = Blueprint("products", url_prefix="/")
product = Blueprint("product", url_prefix="/")
buy_product = Blueprint("buy_product", url_prefix="/buy")
product_group = Blueprint.group(buy_product, product, url_prefix="/<product_id:int>")
products_group = Blueprint.group(product_group, products, url_prefix="/products")

@products.get("/")
async def get_products(request):
    return json({"All products": ["product1", "product2", "...", "productN"]})

@product.get("/")
async def get_product(request, product_id):
    return json({f"Product {product_id}": "Product information"})

@buy_product.get("/")
async def buy_product(request, product_id):
    return json({"info":f"Product {product_id} buyed"})

