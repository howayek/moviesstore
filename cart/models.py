from django.db import models
from django.conf import settings
from movies.models import Movie

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user}'

class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
