from sanic import Blueprint

from .login import login
from .users import users_group
from .products import products_group


api = Blueprint.group(login, users_group, products_group, url_prefix="/api")