from django import forms
from core.models.transaction import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'category', 'paid_by', 'participants', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'participants': forms.CheckboxSelectMultiple,
        }
