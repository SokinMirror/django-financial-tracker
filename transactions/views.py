from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm  # 2. Import your new form
from django.db.models import Sum

def transaction_list(request):
    # Check if the form is being submitted
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new transaction
            return redirect('transaction-list') # Redirect to the same page

    # If it's a normal GET request, show a blank form
    form = TransactionForm()

    transactions = Transaction.objects.all().order_by('-date')

    # 2. CALCULATE THE TOTAL
    # This gets the sum of the 'amount' column
    # The .get() is to handle the case where there are no transactions (total=None)
    total_balance = transactions.aggregate(Sum('amount')).get('amount__sum') or 0.00

    context = {
        'transactions': transactions,
        'form': form,  # Add the form to the context
        'total_balance': total_balance,  # Add the total balance to the context
    }
    return render(request, 'transactions/transaction_list.html', context)


# NEW DELETE VIEW
def transaction_delete(request, pk):
    # Find the object or return a 404 error if not found
    transaction = get_object_or_404(Transaction, pk=pk)

    # Only allow deletion if it's a POST request
    if request.method == 'POST':
        transaction.delete()

    # Redirect back to the main list
    return redirect('transaction-list')


# NEW EDIT VIEW
def transaction_edit(request, pk):
    # Get the specific transaction object we want to edit
    transaction = get_object_or_404(Transaction, pk=pk)

    # Check if the form is being submitted
    if request.method == 'POST':
       # Load the form with the submitted data AND the instance we are editing
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save() # 4. Save the changes to the *existing* transaction
            return redirect('transaction-list')

    # If it's a GET request (just loading the page),
    # load the form with the transaction's *existing* data
    else:
        form = TransactionForm(instance=transaction)

    # Render the edit page template
    return render(request, 'transactions/transaction_edit.html', {'form': form})