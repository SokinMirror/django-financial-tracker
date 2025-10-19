from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()