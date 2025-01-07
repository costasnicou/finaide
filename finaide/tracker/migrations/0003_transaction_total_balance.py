# Generated by Django 5.1.4 on 2025-01-07 20:21

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_alter_wallet_category_fat'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='total_balance',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15),
        ),
    ]
