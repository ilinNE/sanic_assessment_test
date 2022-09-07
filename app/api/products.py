from sanic import Blueprint, json

from models import Product, Bill
from permissions import is_authenticated, admin_only

products = Blueprint("products", url_prefix="/")
product = Blueprint("product", url_prefix="/<product_id:int>")
products_group = Blueprint.group(product, products, url_prefix="/products")

@products.get("/")
@is_authenticated
async def get_products(request):
    products = await Product.all()
    return json({"All products": [product.to_dict() for product in products]})

@products.post("/")
@admin_only
async def create_product(request):
    label = request.json.get('label')
    price = request.json.get('price')
    description = request.json.get('description')
    new_product = await Product.create(
        label=label,
        price=price,
        description=description,
    )
    return json({"Product created": new_product.to_dict()}, status=201)

@product.get("/")
@is_authenticated
async def get_product(request, product_id):
    product = await Product.get(id=product_id)
    return json({
        "product": product.to_dict()
    })

@product.post("/buy_product")
@is_authenticated
async def buy_product(request, product_id):
    bill_id = request.json.get('bill')
    product = await Product.get(id=product_id)
    bill = await Bill.get(id=bill_id)
    bill.balance -= product.price
    await bill.save()
    return json(
        {"info":f"Product {product_id} buyed", "balance": bill.balance}
    )

