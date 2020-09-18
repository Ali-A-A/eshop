from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Billing(models.Model):
    order = models.OneToOneField("Order" , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    notes = models.TextField(blank=True , null=True)
    is_in_progress = models.BooleanField(default=True)

    def __str__(self):
        return str(self.is_in_progress)



class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True , null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        return sum([x.price for x in self.order_row.all()])



class OrderRow(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name="order_row")
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    price = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.product.title