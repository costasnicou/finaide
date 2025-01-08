
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
from .models import Transaction, Wallet, Fat
from .forms import TransactionForm, SignupForm
from django.contrib import messages
from django.contrib.auth import login
from .forms import SignupForm
from decimal import Decimal

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm


def homepage(request):
    return render(request, 'tracker/homepage.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            return redirect('login')  # Redirect to your desired page
    else:
        form = SignupForm()

    return render(request, 'tracker/signup.html', {'form': form})


@login_required
def dashboard(request):

    if request.method == 'POST':
        
        if 'submit_wallet_form' in request.POST:
            wallet_form_submitted = WalletForm(request.POST)
            if wallet_form_submitted.is_valid():
                wallet = wallet_form_submitted.save(commit=False)
                wallet.user = request.user
                wallet.save()
                return redirect('dashboard')
        elif 'submit_transaction_form' in request.POST:
            transaction_form_submitted = TransactionForm(request.POST, user=request.user)
            if transaction_form_submitted.is_valid():
                transaction = transaction_form_submitted.save(commit=False)
                wallet = transaction_form_submitted.cleaned_data['wallet']
                transaction.wallet = wallet
                if transaction.type == 'Income':
                    wallet.balance += Decimal(transaction.amount)
                else:
                    wallet.balance -= Decimal(transaction.amount)
                total_balance = Decimal(sum(Decimal(w.balance) for w in Wallet.objects.filter(user=request.user)))
                if transaction.type == 'Income':
                    transaction.total_balance = total_balance + Decimal(transaction.amount)
                else:
                    transaction.total_balance = total_balance - Decimal(transaction.amount)
                transaction.save()
                wallet.save()
                return redirect('dashboard')
        
        transaction_id = request.POST.get('transaction_id')
        if transaction_id:
            transaction = get_object_or_404(Transaction, id=transaction_id)
            original_wallet = transaction.wallet
            original_type = transaction.type
            original_amount = Decimal(transaction.amount)

            transaction_form_submitted = TransactionForm(request.POST, user=request.user, instance=transaction)

            if transaction_form_submitted.is_valid():
                if 'delete_transaction' in request.POST:
                    wallet = transaction.wallet
                    if transaction.type == 'Income':
                        wallet.balance -= Decimal(transaction.amount)
                    elif transaction.type == 'Expense':
                        wallet.balance += Decimal(transaction.amount)
                    wallet.save()
                    transaction.delete()
                    messages.success(request, "Transaction deleted successfully!")
                    return redirect('dashboard')

                updated_transaction = transaction_form_submitted.save(commit=False)
                if original_wallet != updated_transaction.wallet:
                    if original_type == 'Income':
                        original_wallet.balance -= Decimal(original_amount)
                    elif original_type == 'Expense':
                        original_wallet.balance += Decimal(original_amount)
                    original_wallet.save()

                    new_wallet = updated_transaction.wallet
                    if updated_transaction.type == 'Income':
                        new_wallet.balance += Decimal(updated_transaction.amount)
                    elif updated_transaction.type == 'Expense':
                        new_wallet.balance -= Decimal(updated_transaction.amount)
                    new_wallet.save()
                else:
                    if original_type == 'Income':
                        original_wallet.balance -= Decimal(original_amount)
                    elif original_type == 'Expense':
                        original_wallet.balance += Decimal(original_amount)

                    if updated_transaction.type == 'Income':
                        original_wallet.balance += Decimal(updated_transaction.amount)
                    elif updated_transaction.type == 'Expense':
                        original_wallet.balance -= Decimal(updated_transaction.amount)

                    original_wallet.save()

                total_balance = Decimal(sum(Decimal(w.balance) for w in Wallet.objects.filter(user=request.user)))
                updated_transaction.total_balance = total_balance
                updated_transaction.save()
                messages.success(request, "Transaction updated successfully!")
                return redirect('dashboard')
       
        wallet_id = request.POST.get('wallet_id')

        if wallet_id:
            wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)

            if 'delete_wallet' in request.POST:
                wallet.delete()
                messages.success(request, "Wallet deleted successfully!")
                return redirect('dashboard')

            wallet_form_submitted = WalletForm(request.POST, instance=wallet)
            
            initial_balance = Decimal(wallet.balance)
      
            if wallet_form_submitted.is_valid():
                updated_balance = Decimal(wallet_form_submitted.cleaned_data.get('balance'))
                fat_amount = Decimal(wallet.update_fat_balance(initial_balance))
               
                print(f'Fat Amount: {fat_amount}')
                #expense transaction    
                if updated_balance < initial_balance: 
                    print('---------EXPENSE TRANSACTION---------')
                    previous_expense_sum = Decimal(Transaction.objects.filter(
                        wallet=wallet,
                        category='Balance Adjustment',
                        type='Expense'
                    ).aggregate(total_expenses=Sum('amount'))['total_expenses'] or Decimal('0.00'))
                    print(f'Previous Expense: {previous_expense_sum}')

                    previous_income_sum = Decimal(Transaction.objects.filter(
                        wallet=wallet,
                        type='Income',
                        category='Balance Adjustment',
                    ).aggregate(total_income=Sum('amount'))['total_income'] or Decimal('0.00'))
                    print(f'Previous Income Sum: {previous_income_sum}')
                    
                    adjusted_amount = Decimal(abs(fat_amount)) - Decimal(abs(previous_expense_sum))
                    adjusted_amount = Decimal(fat_amount) + Decimal(abs(previous_income_sum)) - Decimal(abs(previous_expense_sum))
                    adjusted_amount = Decimal(abs(adjusted_amount))
                    print(f'Adjusted Amount {adjusted_amount}')
                    total_balance = Decimal(sum(Decimal(w.balance) for w in Wallet.objects.filter(user=request.user)))

                    Transaction.objects.create(
                            wallet=wallet,
                            type='Expense',
                            category='Balance Adjustment',
                            amount=adjusted_amount,
                            total_balance=total_balance - adjusted_amount,
                    )
                    messages.success(request, "Wallet updated with an expense record!")
                    
                #income transaction         
                elif updated_balance > initial_balance:
                    print('---------EXPENSE TRANSACTION---------')
                    previous_income_sum = Decimal(Transaction.objects.filter(
                        wallet=wallet,
                        type='Income',
                        category='Balance Adjustment',
                    ).aggregate(total_income=Sum('amount'))['total_income'] or Decimal('0.00'))
                    print(f'Previous Income Sum: {previous_income_sum}')

                    previous_expense_sum = Decimal(Transaction.objects.filter(
                        wallet=wallet,
                        category='Balance Adjustment',
                        type='Expense'
                    ).aggregate(total_expenses=Sum('amount'))['total_expenses'] or Decimal('0.00'))
                    print(f'Previous Expense Sum: {previous_expense_sum}')


                    adjusted_amount = Decimal(fat_amount) + Decimal(abs(previous_income_sum)) - Decimal(abs(previous_expense_sum))
                    adjusted_amount = Decimal(abs(adjusted_amount))
                    print(f'Adjusted Amount: {adjusted_amount}')
                    if adjusted_amount > 0:
                        total_balance = Decimal(sum(Decimal(w.balance) for w in Wallet.objects.filter(user=request.user)))
                        Transaction.objects.create(
                            wallet=wallet,
                            type='Income',
                            category='Balance Adjustment',
                            amount=adjusted_amount,
                            total_balance=total_balance + adjusted_amount,
                        )
                        messages.success(request, "Wallet updated with an income record!")
                    else:
                        messages.info(request, "No additional income adjustment required.")
                                
                wallet.save()
                messages.success(request, "Wallet updated successfully!")
                return redirect('dashboard')                       
    
    wallet_form = WalletForm()
    transaction_form = TransactionForm(user=request.user)

    wallets = Wallet.objects.filter(user=request.user)
    wallet_forms = {wallet.id: WalletForm(instance=wallet) for wallet in wallets}
    transactions = Transaction.objects.filter(wallet__user=request.user).order_by('-timestamp')
    for transaction in transactions:
        transaction.edit_form = TransactionForm(instance=transaction, user=request.user)
    
    total_fat = Decimal(Fat.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00'))
    total_balance = Decimal(sum(Decimal(wallet.balance) for wallet in wallets))
    total_income = Decimal(Transaction.objects.filter(wallet__user=request.user, type='Income').aggregate(total=Sum('amount'))['total'] or Decimal('0.00'))
    total_expenses = Decimal(Transaction.objects.filter(wallet__user=request.user, type='Expense').aggregate(total=Sum('amount'))['total'] or Decimal('0.00'))
    net_balance = Decimal(total_income) - Decimal(total_expenses)
    
    return render(request, 'tracker/dashboard.html', {
        'wallets': wallets,
        'wallet_forms': wallet_forms,
        'transactions': transactions,
        'total_balance': total_balance,
        'wallet_form': wallet_form,
        'transaction_form': transaction_form,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'total_fat': total_fat,
    })
