from django.db import models

class Transaction(models.Model):
    description = models.CharField(max_length=100)
    # Use DecimalField for money! It avoids floating-point rounding errors.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True) # Automatically sets the date when created

    def __str__(self):
        return self.description