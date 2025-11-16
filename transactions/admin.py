from django.contrib import admin
# 1. ADD 'Account' TO THIS IMPORT LIST
from .models import Transaction, Category, Loan, Account 

# This class customizes how the Transaction admin page looks
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'category', 'account', 'date')
    readonly_fields = ('date', 'raw_row_data')
    # Add filters to make it easier to browse
    list_filter = ('account', 'category')

# Register the models
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
admin.site.register(Loan)
admin.site.register(Account) # 2. ADD THIS LINE TO REGISTER YOUR NEW MODEL