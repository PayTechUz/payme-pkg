from django.db import models

class Order(models.Model):
    """
    Order model to test the transaction model.
    """
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    total_cost = models.IntegerField()
    payment_method = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)