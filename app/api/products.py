from sanic import Blueprint, json

from models import Product, Bill
products = Blueprint("products", url_prefix="/")
product = Blueprint("product", url_prefix="/")
buy_product = Blueprint("buy_product", url_prefix="/buy")
product_group = Blueprint.group(buy_product, product, url_prefix="/<product_id:int>")
products_group = Blueprint.group(product_group, products, url_prefix="/products")

@products.get("/")
async def get_products(request):
    products = await Product.all()
    return json({"All products": [product.to_dict() for product in products]})

@products.post("/")
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
async def get_product(request, product_id):
    product = await Product.get(id=product_id)
    return json({f"Product {product_id}": product.to_dict()})

@buy_product.post("/")
async def buy_product(request, product_id):
    bill_id = request.json.get('bill')
    product = await Product.get(id=product_id)
    bill = await Bill.get(id=bill_id)
    bill.balance -= product.price
    await bill.save()
    return json(
        {"info":f"Product {product_id} buyed", "balance": bill.balance}
    )

