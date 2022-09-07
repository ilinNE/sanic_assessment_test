from email.policy import default
from tortoise import Model, fields


class Users(Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=32, unique=True)
    password = fields.CharField(max_length=32)
    is_active = fields.BooleanField(default=False)
    is_admin= fields.BooleanField(default=False)
    activation_link = fields.CharField(max_length=64, default='', blank=True)

    def __str__(self):
        return f"User {self.id}: {self.login}"
    
    def to_dict(self):
        return {"id": self.id, "login":self.login, "is_active": self.is_active, "is_admin": self.is_admin} 


class Product(Model):
    id = fields.IntField(pk=True)
    label = fields.CharField(max_length=64)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Product {self.id}: {self.label}"

    def to_dict(self):
        product_as_dict = {
            "id": self.id,
            "label": self.label,
            "price": self.price,
            "desctiption": self.description
        }
        return product_as_dict


class Bill(Model):
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField(
        'models.Users',
        related_name='bills',
        on_delete=fields.CASCADE
    )
    balance = fields.DecimalField(max_digits=15, decimal_places=2, default=0)

    def to_dict(self):
        bill_as_dict = {
            "bill id:": self.id,
            "balance:": self.balance
        }
        return bill_as_dict

    def  __str__(self):
        return f"Bill {self.id}"


class Transaction(Model): 
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField(
        'models.Users',
        related_name='transactions',
        on_delete=fields.CASCADE
    )
    bill = fields.ForeignKeyField(
        'models.Bill',
        related_name='transactions',
        on_delete=fields.CASCADE
    )
    amount = fields.DecimalField(max_digits=15, decimal_places=2)

    def to_dict(self):
        transaction_as_dict = {
            "transaction id": self.id,
            "amount": self.amount
        }
        return transaction_as_dict
