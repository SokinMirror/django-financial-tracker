from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    description = models.CharField(max_length=100)
    # Use DecimalField for money! It avoids floating-point rounding errors.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True) # Automatically sets the date when created
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.description
    
class Loan(models.Model):
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_day = models.IntegerField(default=1)

    def __str__(self):
        return self.name

# Additional model to track payments made towards loans

class Account(models.Model):
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    raw_row_data = models.TextField(null=True, blank=True)
    
    # 2. ADD THIS FIELD TO LINK THE MODELS
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.description
    
class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    payment_month = models.IntegerField()
    payment_year = models.IntegerField()

    def __str__(self):
        return f"Payment for {self.loan.name} in {self.payment_month}/{self.payment_year}"
