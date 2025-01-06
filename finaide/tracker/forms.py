from django import forms
from .models import Wallet, Transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['wallet', 'type', 'category', 'amount']
        widgets = {
            'wallet': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Extract 'user' from kwargs if present
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Call the parent class's __init__
        if user:
            # Filter the queryset for wallets to only include the logged-in user's wallets
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)
        else:
            # Default to an empty queryset if no user is provided
            self.fields['wallet'].queryset = Wallet.objects.none()


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Enter a strong password.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above for verification.",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'category', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ['type', 'category', 'amount']
