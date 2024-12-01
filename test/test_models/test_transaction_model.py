from typing import List, Type
import pytest

from django.core.management import call_command
from django.db.utils import IntegrityError

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

    @pytest.mark.django_db(transaction=True)
    def test_create_transaction_invalid_order(self) -> None:
        """
        Test creating a new transaction with an invalid order.
        """
        with pytest.raises(IntegrityError):
            PaymeTransactions.objects.create(
                transaction_id="12345",
                account=None,
                amount=100.00,
                state=PaymeTransactions.CREATED
            )

    @pytest.mark.django_db(transaction=True)
    def test_create_transaction_invalid_amount(self) -> None:
        """
        Test creating a new transaction with an invalid amount.
        """
        order = create_order()

        with pytest.raises(IntegrityError):
            PaymeTransactions.objects.create(
                transaction_id="12345",
                account=order,
                amount=None,
                state=PaymeTransactions.CREATED
            )

    @pytest.mark.django_db(transaction=True)
    def test_create_transaction_invalid_state(self) -> None:
        """
        Test creating a new transaction with an invalid state.
        """
        order = create_order()

        with pytest.raises(IntegrityError):
            PaymeTransactions.objects.create(
                transaction_id="12345",
                account=order,
                amount=100.00,
                state=None
           )
            
    @pytest.mark.django_db(transaction=True)
    def test_string_represetation_of_transaction(self) -> None:
        """
        Test the string representation of a transaction.
        """
        order = create_order()
        transaction = create_transaction(order)

        assert str(transaction) == f"Payme Transaction #12345 Account: {order} - {transaction.state}"

    @pytest.mark.django_db(transaction=True)
    def test_is_performed(self) -> None:
        """
        Test checking if a transaction is performed.
        """
        order = create_order()
        transaction = create_transaction(order)

        assert not transaction.is_performed()

        transaction.state = PaymeTransactions.SUCCESSFULLY
        assert transaction.is_performed()

    @pytest.mark.django_db(transaction=True)
    def test_is_cancelled(self) -> None:
        """
        Test checking if a transaction is cancelled.
        """
        order = create_order()
        transaction = create_transaction(order)

        assert not transaction.is_cancelled() # C

        transaction.state = PaymeTransactions.CANCELED
        assert transaction.is_cancelled()

        transaction.state = PaymeTransactions.CANCELED_DURING_INIT
        assert transaction.is_cancelled()

    @pytest.mark.django_db(transaction=True)
    def test_is_created(self) -> None:
        """
        Test checking if a transaction is created.
        """
        order = create_order()
        transaction = create_transaction(order)

        assert transaction.is_created()

        transaction.state = PaymeTransactions.SUCCESSFULLY
        assert not transaction.is_created()
    
    @pytest.mark.django_db(transaction=True)
    def test_is_created_in_payme(self) -> None:
        """
        Test checking if a transaction is created in Payme.
        """
        order = create_order()
        transaction = create_transaction(order)

        assert not transaction.is_created_in_payme()

        transaction.state = PaymeTransactions.INITIATING
        assert transaction.is_created_in_payme()

    @pytest.mark.django_db(transaction=True)
    def test_mark_as_cancelled(self) -> None:
        """
        Test marking a transaction as cancelled.
        """
        order = create_order()
        transaction = create_transaction(order)

        assert not transaction.is_cancelled()

        transaction.mark_as_cancelled(1, PaymeTransactions.CANCELED)

        assert transaction.is_cancelled()
        assert transaction.state == PaymeTransactions.CANCELED
