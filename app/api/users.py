import uuid

from sanic import Blueprint, json

from models import Users, Bill, Transaction
from permissions import is_authenticated, admin_only, owner_or_admin

user = Blueprint("user", url_prefix="/<user_id:int>")
users = Blueprint("users", url_prefix="/")
users_group = Blueprint.group(user, users, url_prefix="/users")

@user.post("/bills")
@owner_or_admin
async def create_bill(request, user_id):
    user =request.ctx.user
    new_bill: Bill = await Bill.create(owner=user)
    return json({f"Bill created": str(new_bill)})

@user.get("/bills")
@owner_or_admin
async def get_bills(request, user_id):
    user =request.ctx.user
    bills = await Bill.filter(owner=user)
    return json({f"Bills for user {request.ctx.user}": [bill.to_dict() for bill in bills]})

@user.post("/transactions")
@owner_or_admin
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

@user.get("/transactions")
@owner_or_admin
async def get_transactions(request, user_id):
    transactions = await Transaction.filter(owner_id=user_id)
    return json({f"Transactions for user {user_id}": [transaction.to_dict() for transaction in transactions]})

@users.post("/")
async def create_user(request):
    login = request.json.get('login')
    password = request.json.get('password')
    user = await Users.create(
        login=login,
        password=password, 
        activation_link = uuid.uuid4()
    )
    return json({"User created": user.to_dict(), "Activation link": f"/api/login/{user.activation_link}"}, 201)


@users.get("/")
@admin_only
async def get_users(request):
    users = await Users.all()
    return json({"users": [user.to_dict() for user in users ]})


@user.get("/")
@owner_or_admin
async def get_user(request, user_id):
    user = await Users.get(id=user_id)
    return json({f"User {user.id}": user.to_dict()})

@user.get("/activate")
@admin_only
async def activate_user(request, user_id):
    user = await Users.get(id=user_id)
    user.is_active = True
    await user.save()
    return json({"message": f"user {user} activated"})


@user.get("/deactivate")
@admin_only
async def activate_user(request, user_id):
    user = await Users.get(id=user_id)
    user.is_active = False
    await user.save()
    return json({"message": f"user {user} deactivated"})   

