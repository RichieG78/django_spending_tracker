"""Forms for expense and income entry screens."""

from django import forms

from .models import Expense, Income


class ExpenseCreateForm(forms.ModelForm):
    """Styled expense create form with constrained frequency choices."""

    # Offer clear recurrence options instead of free-form text entry.
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('one off', 'One off'),
    ]

    frequency = forms.ChoiceField(
        choices=FREQUENCY_CHOICES,
        initial='monthly',
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'frequency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Rent'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
        }


class IncomeCreateForm(forms.ModelForm):
    """Styled income create form with constrained recurrence choices."""

    # Keep the same recurrence vocabulary across income and expense forms.
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('one off', 'One off'),
    ]
    GROSS_NET_CHOICES = [
        ('gross', 'Gross'),
        ('net', 'Net'),
    ]

    frequency = forms.ChoiceField(
        choices=FREQUENCY_CHOICES,
        initial='monthly',
        widget=forms.RadioSelect,
    )
    gross_net = forms.ChoiceField(
        choices=GROSS_NET_CHOICES,
        initial='net',
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Income
        fields = ['name', 'amount', 'frequency', 'type', 'gross_net']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Salary'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
            'type': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Employment'}),
        }
