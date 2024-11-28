from typing import List, Type
import pytest

from django.core.management import call_command

from payme.models import PaymeTransactions

from test.models import Order  # Import the Order model

def create_order() -> Type[Order]:
    """
    Helper method to create a new order object.
    """
    return Order.objects.create(
        customer_name="John Doe",
        address="123 Main St",
        total_cost=150,
        payment_method="Credit Card",
        is_paid=True
    )

def create_transaction(order: Type[Order]) -> Type[PaymeTransactions]:
    """
    Helper method to create a new transaction object.
    """
    return PaymeTransactions.objects.create(
        transaction_id="12345",
        account=order,
        amount=100.00,
        state=PaymeTransactions.CREATED
    )

class TestTransactionModel:
    """
    Unit tests for the PaymeTransactions model.
    """

    @pytest.mark.django_db(transaction=True)
    def test_create_transaction(self) -> None:
        """
        Test creating a new transaction model.
        """
        order = create_order()
        transaction = create_transaction(order)

        assert transaction.transaction_id == "12345"
        assert transaction.amount == 100.00
        assert transaction.state == PaymeTransactions.CREATED
        assert transaction.account == order

    @pytest.mark.django_db(transaction=True)
    def test_get_by_transaction_id(self) -> None:
        """
        Test getting a transaction by its transaction ID.
        """
        order = create_order()
        transaction = create_transaction(order)

        # Get the transaction by its ID
        retrieved_transaction = PaymeTransactions.get_by_transaction_id("12345")

        assert retrieved_transaction == transaction