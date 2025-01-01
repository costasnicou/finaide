from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from .forms import WalletForm, TransactionForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404

from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm


def homepage(request):
    return render(request, 'tracker/homepage.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect('dashboard')  # Redirect to the dashboard after signup
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})


@login_required
def dashboard(request):
    wallets = Wallet.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(wallet__user=request.user).order_by('-timestamp')  # Recent transactions first
    total_balance = sum(wallet.balance for wallet in wallets)
    return render(request, 'tracker/dashboard.html', {
        'wallets': wallets,
        'transactions': transactions,
        'total_balance': total_balance,
    })

@login_required
def add_wallet(request):
    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
            return redirect('dashboard')
    else:
        form = WalletForm()
    return render(request, 'tracker/add_wallet.html', {'form': form})

@login_required
def add_transaction(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.wallet = wallet
            if transaction.type == 'Income':
                wallet.balance += transaction.amount
            else:
                wallet.balance -= transaction.amount
            wallet.save()
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form, 'wallet': wallet})

# delete wallet
@login_required
def delete_wallet(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)

    # Deduct the wallet balance from the total balance before deletion
    wallet_balance = wallet.balance

    if request.method == 'POST':
        wallet.delete()
        return redirect('dashboard')

    return render(request, 'tracker/confirm_delete_wallet.html', {'wallet': wallet})
