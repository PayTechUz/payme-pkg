# Generated by Django 5.1.2 on 2024-10-18 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymeTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('state', models.IntegerField(choices=[(0, 'CREATED'), (1, 'WITHDRAWAL_IN_PROGRESS_1'), (2, 'WITHDRAWAL_IN_PROGRESS_2'), (3, 'WITHDRAWAL_CLOSING'), (4, 'SUCCESS'), (20, 'WAITING_TO_BE_CHECKED'), (21, 'WAITING_TO_BE_CANCELLED_1'), (30, 'WAITING_TO_BE_CANCELLED_2'), (50, 'CANCELED'), (-2, 'CANCELLED_WITHDRAWAL_IN_PROGRESS_2'), (-1, 'CANCELLED_AFTER_WITHDRAWAL_IN_PROGRESS_1')], default=0)),
                ('cancel_reason', models.IntegerField(blank=True, choices=[(1, 'RECIPIENT_NOT_FOUND'), (2, 'DEBIT_OPERATION_FAILED'), (3, 'TRANSACTION_FAILED'), (4, 'TRANSACTION_TIMEOUT'), (5, 'REFUND'), (10, 'UNKNOWN_ERROR')], null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('performed_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('cancelled_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payme_transactions', to='users.client')),
            ],
            options={
                'verbose_name': 'Payme Transaction',
                'verbose_name_plural': 'Payme Transactions',
                'db_table': 'payme_transactions',
                'ordering': ['-created_at'],
            },
        ),
    ]