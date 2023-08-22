# pylint: disable=invalid-name
from django.db import migrations, models


class Migration(migrations.Migration):
    # pylint: disable=missing-class-docstring
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MerchatTransactionsModel',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')
                ),
                ('_id', models.CharField(max_length=255, null=True)),
                ('transaction_id', models.CharField(max_length=255, null=True)),
                ('order_id', models.BigIntegerField(blank=True, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('time', models.BigIntegerField(blank=True, null=True)),
                ('perform_time', models.BigIntegerField(default=0, null=True)),
                ('cancel_time', models.BigIntegerField(default=0, null=True)),
                ('state', models.IntegerField(default=1, null=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at_ms', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')
                 ),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
