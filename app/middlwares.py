from re import U
import jwt


from auth import check_token, extract_user_info_from_token

async def is_authenticated(request):
    request.ctx.is_authenticated = check_token(request)


async def extract_user_info(request):
    if not request.ctx.is_authenticated:
        return
    user_info = extract_user_info_from_token(request)
    request.ctx.user_id = user_info['id']
    request.ctx.user_is_active = user_info['is_active']
    request.ctx.user_is_admin = user_info['is_admin']