from django import forms
from .models import Transaction
from .models import Loan

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'category']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['name', 'total_amount', 'monthly_payment']