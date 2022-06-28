from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Product(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="products"
    )
