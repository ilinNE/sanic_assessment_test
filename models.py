from email.policy import default
from tortoise import Model, fields


class Users(Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=32, unique=True)
    password = fields.CharField(max_length=32)
    is_active = fields.BooleanField(default=False)
    is_admin= fields.BooleanField(default=False)

    def __str__(self):
        return f"User {self.id}: {self.login}"


class Product(Model):
    id = fields.IntField(pk=True)
    label = fields.CharField(max_length=64)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Product {self.id}: {self.label}"


class Bill(Model):
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField(
        'models.Users',
        related_name='bills',
        on_delete=fields.CASCADE
    )
    balance = fields.DecimalField(max_digits=15, decimal_places=2, default=0)

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

    
