from django.db import models
from dateutil.relativedelta import relativedelta
import datetime

# --- MODELS ARE NOW IN THE CORRECT ORDER ---

# These models stand alone, so they go first.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Account(models.Model):
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(default=datetime.date.today)
    installments_count = models.IntegerField(default=0)
    # payment_due_day is from your old model, you can uncomment it if you need it
    # payment_due_day = models.IntegerField(default=1) 

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
    # 1. Save the Loan object itself first.
        #    This is important so it has an 'id' for the next steps.
        super().save(*args, **kwargs)
        
        # 2. Delete all (0 or more) existing installments linked to this loan.
        #    We can use 'self.installments' because of the related_name="installments"
        #    on the Installment model's 'loan' field.
        self.installments.all().delete()
        
        # 3. Re-create the entire installment schedule from scratch.
        for i in range(self.installments_count):
            # Add 'i' months to the start date
            due_date = self.start_date + relativedelta(months=i)
            Installment.objects.create(
                loan=self,
                due_date=due_date
            )

    # This method auto-generates the installment schedule
    def save(self, *args, **kwargs):
        # 1. Check if this is a new loan (no 'id' yet)
        is_new = self.id is None 

        # 2. Save the loan object itself (so it gets an id)
        super().save(*args, **kwargs) # This saves the Loan

        # 3. If it was new, create its installments
        if is_new:
            for i in range(self.installments_count):
                # Add 'i' months to the start date
                due_date = self.start_date + relativedelta(months=i)
                Installment.objects.create(
                    loan=self,
                    due_date=due_date
                )

# --- TRANSACTION MODEL (MERGED) ---
# This is now defined only ONCE
class Transaction(models.Model):
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    raw_row_data = models.TextField(null=True, blank=True)
    
    # Links to other models
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.description

# --- INSTALLMENT MODEL (CLEANED) ---
# This model must be defined LAST
class Installment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]

    # related_name="installments" is important for the Loan's save method
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="installments")
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    # This is the ONLY link to a transaction
    linked_transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    
    # We don't need payment_month/year because we have due_date
    # We don't need the extra 'transaction' field

    def __str__(self):
        return f"{self.loan.name} - {self.due_date.strftime('%B %Y')}"