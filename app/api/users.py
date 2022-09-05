from sanic import Blueprint, json

from models import Users, Bill, Transaction

bills = Blueprint("bills", url_prefix="/bills")
user = Blueprint("user", url_prefix="/")
transactions = Blueprint("transactions", url_prefix="/transactions")
users = Blueprint("users", url_prefix="/")
user_group = Blueprint.group(transactions, bills, user, url_prefix="/<user_id:int>")
users_group = Blueprint.group(user_group, users, url_prefix="/users")


@bills.post("/")
async def create_bill(request, user_id):
    user =request.ctx.user
    new_bill: Bill = await Bill.create(owner=user)
    return json({f"Bill created": str(new_bill)})

@bills.get("/")
async def get_bills(request, user_id):
    user =request.ctx.user
    bills = await Bill.filter(owner=user)
    return json({f"Bills for user {request.ctx.user}": [bill.to_dict() for bill in bills]})

@transactions.post("/")
async def create_transaction(request, user_id):
    user =request.ctx.user
    amount = request.json.get('amount')
    bill_id = request.json.get('bill_id')
    new_transaction = await Transaction.create(
        owner=user,
        amount=amount,
        bill_id=bill_id
    )
    return json({"Transaction created": new_transaction.to_dict()})

@transactions.get("/")
async def get_transactions(request, user_id):
    transactions = await Transaction.filter(owner_id=user_id)
    return json({f"Transactions for user {user_id}": [transaction.to_dict() for transaction in transactions]})

@users.post("/")
async def create_user(request):
    login = request.json.get('login')
    password = request.json.get('password')
    user = await Users.create(
        login=login,
        password=password 
    )
    return json({"User created": user.to_dict()}, 201)

@users.get("/")
async def get_user(request):
    users = await Users.all()
    return json({"users": [user.to_dict() for user in users ]})


@user.get("/")
async def get_user(request, user_id):
    user = await Users.get(id=user_id)
    return json({f"User {user.id}": user.to_dict()})
