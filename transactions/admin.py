from django.contrib import admin
from .models import Transaction, Category, Loan  # Import your Transaction model

# This one line tells Django to show the Transaction model in the admin
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Loan)