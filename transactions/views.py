import csv
import io
import chardet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Category, Loan
from .forms import TransactionForm, CSVUploadForm
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

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            # --- START ENCODING FIX ---
            # 1. Read the file as raw bytes
            raw_data = csv_file.read()
            
            if not raw_data:
                context = {'form': form, 'error': 'The file is empty.'}
                return render(request, 'transactions/upload_csv.html', context)

            # 2. Let chardet detect the encoding
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            print(f"--- Detected Encoding: {encoding} ---")

            # 3. Decode using the detected encoding
            try:
                data_set = raw_data.decode(encoding)
            except (LookupError, TypeError):
                # Fallback if chardet gives a bad alias
                data_set = raw_data.decode('iso-8859-7', errors='replace')
            # --- END ENCODING FIX ---
            
            io_string = io.StringIO(data_set)
            
            try:
                # Skip the 6 header rows
                for _ in range(6):
                    next(io_string)
            except StopIteration:
                context = {'form': form, 'error': 'The file is empty or has too few rows.'}
                return render(request, 'transactions/upload_csv.html', context)
            
            # --- START CSV READER SETUP ---
            # Use the correct semicolon delimiter
            csv_reader = csv.reader(io_string, delimiter=';', quotechar='"')

            print("--- STARTING CSV IMPORT ---")
            
            for i, row in enumerate(csv_reader):
                
                if not row:
                    print(f"Row {i}: SKIPPED (empty)")
                    continue

                try:
                    # Column C = 2 (Description)
                    # Column G = 6 (Amount)
                    # Column H = 7 (Sign)
                    description = row[2].strip()
                    amount_str = row[6].strip()
                    type_str = row[7].strip()

                    # --- START NUMBER FORMAT FIX ---
                    # 1. Remove any thousand separators (like '.')
                    # 2. Replace the decimal comma with a dot
                    amount_str_cleaned = amount_str.replace('.', '').replace(',', '.')
                    amount = float(amount_str_cleaned)
                    # --- END NUMBER FORMAT FIX ---

                    # --- START CHARGE/INCOME FIX ---
                    # Use the Greek Chi 'Χ'.
                    if type_str == 'Χ':
                        amount = -amount
                    # --- END CHARGE/INCOME FIX ---

                except (IndexError, ValueError) as e:
                    print(f"Row {i}: SKIPPED due to error: {e} | Data: {row}")
                    continue
                
                # --- START DATA ANALYSIS (Categorization) ---
                category = None
                if 'CΑFΕΤΕΧ' in description.upper():
                    category, _ = Category.objects.get_or_create(name='Coffee')
                elif 'ΑΒ VΑSΙLΟΡΟULΟS' in description.upper() or 'ΜΥ ΜΑRΚΕΤ' in description.upper():
                    category, _ = Category.objects.get_or_create(name='Groceries')
                # (Add more categorization rules here)
                # --- END DATA ANALYSIS ---

                Transaction.objects.create(
                    description=description,
                    amount=amount, # This will be positive for income, negative for charges
                    category=category
                )
            
            print("--- FINISHED CSV IMPORT ---")
            return redirect('transaction-list')
    else:
        form = CSVUploadForm()
        
    return render(request, 'transactions/upload_csv.html', {'form': form})


def transaction_summary(request):
    # This is the core query!
    summary = Transaction.objects \
        .values('description') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('total_amount') # Order from biggest expense to biggest income

    # This gives you data like:
    # [
    #   {'category__name': 'Groceries', 'total_amount': -450.50},
    #   {'category__name': 'Coffee', 'total_amount': -80.20},
    #   {'category__name': None, 'total_amount': -50.00},
    #   {'category__name': 'Salary', 'total_amount': 3000.00}
    # ]

    context = {
        'summary': summary
    }
    return render(request, 'transactions/transaction_summary.html', context)