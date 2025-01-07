from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal

class Wallet(models.Model):
    CATEGORY_CHOICES = [
        ('Cash', 'Cash'),
        ('Debit Card', 'Debit Card'),
        ('Credit Card', 'Credit Card'),
        ('Bank Account', 'Bank Account'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    def update_fat_balance(self, initial_balance):
        """
        Updates the corresponding Fat instance's amount based on the wallet's balance.
        """
        # Get or create the 'Fat' instance
        fat, created = Fat.objects.get_or_create(wallet=self)
        # fat_amount = Decimal(fat.amount)
        # Convert both balances to Decimal for precision
        updated_balance_decimal = Decimal(str(self.balance))  # Ensure correct precision with strings
        initial_balance_decimal = Decimal(str(initial_balance))  # Convert wallet's balance to Decimal
       
    

        if created:
           
            # If the Fat instance was just created, initialize its amount
              # If the Fat instance was newly created, initialize its amount to 0.00

            fat.amount = Decimal('0.00')
             # Compare the balances
            # Compare the balances
            if initial_balance_decimal < updated_balance_decimal:
                # If the updated balance is greater, decrease fat amount
                # fat.amount -= 800
                fat.amount -= updated_balance_decimal - initial_balance_decimal

            elif  initial_balance_decimal > updated_balance_decimal:
                # If the updated balance is smaller, increase fat amount
                # fat.amount +=  800
                fat.amount +=  initial_balance_decimal - updated_balance_decimal
           
        else:
            # Compare the balances
            if updated_balance_decimal > initial_balance_decimal:
                # If the updated balance is greater, decrease fat amount
                # fat.amount -= 800
                fat.amount -= updated_balance_decimal - initial_balance_decimal

            else:
                # If the updated balance is smaller, increase fat amount
                # fat.amount +=  800
                fat.amount +=  initial_balance_decimal - updated_balance_decimal
            
        # Save the updated fat instance
        fat.save()

        return fat.amount  # Return the calculated fat amount

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))  # New field

    def __str__(self):
        return f"{self.type} - {self.category} - {self.amount}"



class Fat(models.Model):
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, related_name='fat')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Fat for Wallet: {self.wallet.name} - Amount: {self.amount}"