import jwt
from sanic import Blueprint, json

from models import Users

login = Blueprint("login", url_prefix="/login")


@login.post("/")
async def do_login(request):
    login = request.json.get('login')
    user = await Users.first()
    token = jwt.encode(user.to_dict(), request.app.config.SECRET)
    return json({"access":token.decode('utf-8')})