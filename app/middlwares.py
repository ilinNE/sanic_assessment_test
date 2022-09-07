import jwt

from models import Users
from auth import check_token, parse_token

async def authentication(request):
    if not request.token:
        request.ctx.is_authenticated = False
        return

    try:
        parsed_token = jwt.decode(
            request.token, request.app.config.SECRET, algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidTokenError:
        request.ctx.is_authenticated = False
        return 
    else:
        request.ctx.is_authenticated = True
        request.ctx.user = await Users.get(id=parsed_token['id'])
    




async def extract_user_info(request):
    if not request.ctx.is_authenticated:
        return
    user_info = parse_token(request)
    request.ctx.user = await Users.get(id=user_info['id'])
