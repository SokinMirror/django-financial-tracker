from django.shortcuts import render
from .models import Transaction

def transaction_list(request):
    # 1. Get all transaction objects from the database
    transactions = Transaction.objects.all()

    # 2. Pass the data to the template
    # We'll create this HTML file in the next step
    context = {
        'transactions': transactions
    }
    return render(request, 'transactions/transaction_list.html', context)