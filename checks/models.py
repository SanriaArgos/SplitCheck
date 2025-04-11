from django.db import models
from django.contrib.auth.models import User

class Receipt(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='receipt_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} (id={self.id})"

    def total_amount(self):
        return self.items.aggregate(total=models.Sum('price'))['total'] or 0

class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.name} - {self.price}"

class Participant(models.Model):
    name = models.CharField(max_length=100)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='participants')

    def __str__(self):
        return self.name