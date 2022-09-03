from sanic import Blueprint, json

bills = Blueprint("bills", url_prefix="/bills")
user = Blueprint("user", url_prefix="/")
transactions = Blueprint("transactions", url_prefix="/transactions")
users = Blueprint("users", url_prefix="/")
user_group = Blueprint.group(transactions, bills, user, url_prefix="/<user_id:int>")
users_group = Blueprint.group(user_group, users, url_prefix="/users")


@bills.route("/")
async def get_bills(request, user_id):
    return json({f"bills for user {user_id}": ["bill1", "bill2", "...", "billN"]})

@transactions.route("/")
async def get_bills(request, user_id):
    return json({f"transactions for user {user_id}": ["transaction1", "transaction2", "...", "transactionlN"]})

@users.get("/")
async def get_user(request):
    return json({"users": ["user1", "user2", "...", "userN"]})


@user.get("/")
async def get_user(request, user_id):
    return json({"id": user_id})
