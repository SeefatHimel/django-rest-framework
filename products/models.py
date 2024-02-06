from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    rating = models.PositiveIntegerField()

    def __str__(self, *args):
        return f"{self.name} - Price: {self.price} - Description: {self.description}"
