from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from debts.models import Money
from django.contrib.auth import get_user_model

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = ['payee', 'sum', 'note']
        exclude = ['payer', 'date']
    
    def clean(self):
        cleaned_data = super().clean()
        payee = cleaned_data.get("payee")
        sum = cleaned_data.get("sum")

        if payee and sum:
            users = []
            [users.append(name[0]) for name in get_user_model().objects.values_list('username')]
            if payee not in users:
                raise forms.ValidationError(("Invalid name"), code="invalid")