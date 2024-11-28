import pytest
from django.core.management import call_command
from payme.models import PaymeTransactions
from test.models import Order  # Import the Order model

@pytest.mark.django_db(transaction=True)
def test_create_transaction():
    order = Order.objects.create(
        customer_name="John Doe",
        address="123 Main St",
        total_cost=150,
        payment_method="Credit Card",
        is_paid=True
    )
    transaction = PaymeTransactions.objects.create(
        transaction_id="12345",
        account=order,  # Add the account field
        amount=100.00,
        state=PaymeTransactions.CREATED
    )

    assert transaction.transaction_id == "12345"
    assert transaction.amount == 100.00
    assert transaction.state == PaymeTransactions.CREATED
    assert transaction.account == order  # Assert the account field
