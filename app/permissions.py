from functools import wraps

from sanic.exceptions import Unauthorized, Forbidden

def is_authenticated(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if not request.ctx.is_authenticated:
                raise Unauthorized("Unauthorized")
            if not request.ctx.user.is_active:
                raise Unauthorized("User is not activated")
            response = await f(request, *args, **kwargs)
            return response
        return decorated_function
    return decorator(wrapped)
            
def admin_only(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if not request.ctx.is_authenticated:
                raise Unauthorized("Unauthorized")
            if not request.ctx.user.is_active:
                raise Unauthorized("User is not activated")
            if not request.ctx.user.is_admin:
                raise Forbidden("Only for admin")
            response = await f(request, *args, **kwargs)
            return response
        return decorated_function
    return decorator(wrapped)

def owner_or_admin(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, user_id, *args, **kwargs):
            if not request.ctx.is_authenticated:
                raise Unauthorized("Unauthorized")
            if not request.ctx.user.is_active:
                raise Unauthorized("User is not activated")
            if request.ctx.user.id == user_id or request.ctx.user.is_admin:
                response = await f(request, user_id, *args, **kwargs)
                return response
            raise Forbidden("Only for admin or owner")
        return decorated_function
    return decorator(wrapped)
            