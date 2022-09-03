import logging
import random 

from models import Users, Bill
from sanic import Sanic, response

from tortoise.contrib.sanic import register_tortoise

logging.basicConfig(level=logging.DEBUG)

app = Sanic(__name__)


@app.route("/")
async def list_all(request):
    users = await Users.all()
    return response.json({"users": [str(user) for user in users]})


@app.route("/user")
async def add_user(request):
    user: Users = await Users.create(login=str(random.randint(1,200)), password="123456")
    return response.json(str(user))

@app.route("/bill")
async def add_bill(request):
    user = await Users.first()
    bills = await user.bills.all().values()
    return response.json(bills)


register_tortoise(
    app, db_url="postgres://dev_user:123456@localhost:5432/dev_db", modules={"models": ["models"]}, generate_schemas=True
)


if __name__ == "__main__":
    app.run(port=5000, auto_reload=True)