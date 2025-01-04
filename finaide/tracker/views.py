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
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction, Wallet
from .forms import TransactionForm
from django.contrib import messages

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm


def homepage(request):
    return render(request, 'tracker/homepage.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST,user=request.user)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect('dashboard')  # Redirect to the dashboard after signup
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})


@login_required
def dashboard(request):
    # Process form submission for creating/editing a transaction
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        if 'submit_wallet_form' in request.POST:  # Check which form was submitted
            wallet_form_submitted = WalletForm(request.POST)
            if wallet_form_submitted.is_valid():
                wallet = wallet_form_submitted.save(commit=False)
                wallet.user = request.user
                wallet.save()
                return redirect('dashboard')
        elif 'submit_transaction_form' in request.POST:  # Check which form was submitted
            transaction_form_submitted = TransactionForm(request.POST,user=request.user)
            if transaction_form_submitted.is_valid():
                transaction = transaction_form_submitted.save(commit=False)
                wallet = transaction_form_submitted.cleaned_data['wallet']
                transaction.wallet = wallet
                if transaction.type == 'Income':
                    wallet.balance += transaction.amount
                else:
                    wallet.balance -= transaction.amount
                wallet.save()
                transaction.save()
                return redirect('dashboard')
        # # Handle the edit or delete of a transaction
        # if transaction_id:
        #     # Get the transaction object
        #     transaction = get_object_or_404(Transaction, id=transaction_id)

        #     # Initialize the transaction form with the existing transaction data
        #     transaction_form_submitted = TransactionForm(request.POST, user=request.user, instance=transaction)

        #     if transaction_form_submitted.is_valid():
        #         # If delete button is clicked, delete the transaction
        #         if 'delete_transaction' in request.POST:
        #             transaction.delete()
        #             messages.success(request, "Transaction deleted successfully!")
        #             return redirect('dashboard')
                
        #         # Otherwise, update the transaction
        #         transaction_form_submitted.save()

        #         # Adjust the wallet balance
        #         wallet = transaction.wallet
        #         if transaction.type == 'Income':
        #             wallet.balance += transaction.amount
        #         else:
        #             wallet.balance -= transaction.amount
        #         wallet.save()

        #         messages.success(request, "Transaction updated successfully!")
        #         return redirect('dashboard')












    # Initialize data to display on the dashboard
    wallet_form = WalletForm()
    transaction_form = TransactionForm(user=request.user)

    wallets = Wallet.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(wallet__user=request.user).order_by('-timestamp')
   # Attach a form pre-populated with each transaction's data
    for transaction in transactions:
        transaction.edit_form = TransactionForm(instance=transaction, user=request.user)
    # Calculate totals
    total_balance = sum(wallet.balance for wallet in wallets)
    total_income = Transaction.objects.filter(wallet__user=request.user, type='Income').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Transaction.objects.filter(wallet__user=request.user, type='Expense').aggregate(total=Sum('amount'))['total'] or 0
    net_balance = total_income - total_expenses
    transaction_forms = {transaction.id: TransactionForm(instance=transaction, user=request.user) for transaction in transactions}
    return render(request, 'tracker/dashboard.html', {
        'wallets': wallets,
        'transactions': transactions,
        'total_balance': total_balance,
        'wallet_form': wallet_form,
        'transaction_form': transaction_form,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'transaction_forms':transaction_forms,
    })
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
