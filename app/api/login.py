import jwt
from sanic import Blueprint, json
from sanic.exceptions import Unauthorized

from models import Users
login = Blueprint("login", url_prefix="/login")


@login.post("/")
async def do_login(request):
    login = request.json.get('login')
    password = request.json.get('password')
    user = await Users.get(login=login)
    if user.password != password:
        raise Unauthorized("Wrong password!")
    token = jwt.encode(user.to_dict(), request.app.config.SECRET)
    return json({"access":token.decode('utf-8')})

@login.get("/<activation_uuid:uuid>")
async def activate(request, activation_uuid):
    user = await Users.get(activation_link=activation_uuid)
    user.is_active = True
    user.activation_link = ''
    await user.save()
    return json({"message": "Your account is activated"})

 