from django import forms
from django.contrib.auth.models import User
from core.models.transaction import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'category', 'paid_by', 'participants', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'participants': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Исключаем только пользователя с username='admin', но оставляем всех остальных, даже если они is_staff
        self.fields['paid_by'].queryset = User.objects.exclude(username='admin')
        self.fields['participants'].queryset = User.objects.exclude(username='admin')
