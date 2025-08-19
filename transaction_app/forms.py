from django import forms
from .models import transactionModel


class DepositForm(forms.ModelForm):
    class Meta:
        model = transactionModel
        exclude = ['user']
        