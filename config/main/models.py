
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=100, default="Другие")
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
