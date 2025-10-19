from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Category
from .forms import TransactionForm, CSVUploadForm  # 2. Import your new form
from django.db.models import Sum
import csv # Import Python's built-in CSV module
import io

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

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Read the file in memory
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) # Skip the header row

            from .models import Transaction, Category, Loan

            for row in csv.reader(io_string, delimiter=',', quotechar='"'):
                # Assumes CSV columns are: description, amount
                # You MUST change this to match your bank's CSV
                description = row[0]
                amount = row[1]

                # --- START DATA ANALYSIS ---
                category = None
                if 'COFFEE' in description.upper() or 'STARBUCKS' in description.upper():
                    category = Category.objects.get(name='Coffee')
                elif 'GROCERY' in description.upper():
                    category = Category.objects.get(name='Food')
                # --- END DATA ANALYSIS ---

                # --- LOAN CHECKING LOGIC ---
                # Try to find a loan that matches the description
                # This is a simple check; it can get more complex
                try:
                    loan = Loan.objects.get(name__icontains=description)

                    if amount == loan.monthly_payment:
                        print(f"Successfully paid installment for {loan.name}")
                        # You could also link this transaction to the loan
                    else:
                        print(f"WARNING: Paid {amount} for {loan.name}, but expected {loan.monthly_payment}")
                except Loan.DoesNotExist:
                    pass # Not a loan payment
                # --- END LOAN CHECKING ---

                Transaction.objects.create(
                    description=description,
                    amount=float(amount),
                    category=category
                )
            return redirect('transaction-list')
    else:
        form = CSVUploadForm()

    return render(request, 'transactions/upload_csv.html', {'form': form})