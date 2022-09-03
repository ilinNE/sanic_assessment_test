import logging
import random 
from pathlib import Path

from models import Users, Bill
from sanic import Sanic, response
from tortoise.contrib.sanic import register_tortoise

from api import api
from middlwares import is_authenticated, extract_user_info

logging.basicConfig(level=logging.DEBUG)

config = Path(Path(__file__).parent, 'config.py')
app = Sanic("TestApp")
app.update_config(config)
app.register_middleware(is_authenticated, "request")
app.register_middleware(extract_user_info, "request")

@app.route("/")
async def list_all(request):
    users = await Users.all()
    return response.json({"users": [str(user) for user in users]})


@app.route("/user")
async def add_user(request):
    user: Users = await Users.create(login=str(random.randint(1,200)), password="123456")
    return response.json(str(user))

app.blueprint(api)


register_tortoise(
    app, db_url="postgres://dev_user:123456@localhost:5432/dev_db", modules={"models": ["models"]}, generate_schemas=True
)


if __name__ == "__main__":
    app.run(port=5000, workers=1, auto_reload=True)
