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

def create_transaction(order: Type[Order], id: str="12345") -> Type[PaymeTransactions]:
    """
    Helper method to create a new transaction object.
    """
    return PaymeTransactions.objects.create(
        transaction_id=id,
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
    def test_string_representation_of_transaction(self) -> None:
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

class TestTransactionIntegration:
    """
    Integration tests for the PaymeTransactions model.
    """

    @pytest.mark.django_db(transaction=True)
    def test_payment_transaction_lifecycle(self) -> None:
        """
        Test creating, retrieving, updating, and deleting a payment transaction.
        """
        order = create_order()
                    
        # Create transaction
        transaction = create_transaction(order)
        assert transaction.transaction_id == "12345"
        assert transaction.amount == 100.00
        assert transaction.state == PaymeTransactions.CREATED
                
        # Retrieve transaction
        retrieved_transaction = PaymeTransactions.objects.get(transaction_id="12345")
        assert retrieved_transaction == transaction
                
        # Update transaction
        transaction.amount = 200.00
        transaction.save()
                
        # Retrieve updated transaction
        updated_transaction = PaymeTransactions.objects.get(transaction_id="12345")
        assert updated_transaction.amount == 200.00
                
        # Delete transaction
        transaction.delete()
                
        # Verify deletion
        with pytest.raises(PaymeTransactions.DoesNotExist):
            PaymeTransactions.objects.get(transaction_id="12345")

    @pytest.mark.django_db(transaction=True)
    def test_transaction_cancellation(self) -> None:
        """
        Test cancelling a transaction.
        """
        order = create_order()
        transaction = create_transaction(order)

        assert not transaction.is_cancelled()

        transaction.mark_as_cancelled(1, PaymeTransactions.CANCELED)

        assert transaction.is_cancelled()
        assert transaction.state == PaymeTransactions.CANCELED
    
    @pytest.mark.django_db(transaction=True)
    def test_create_transaction_with_invalid_data(self) -> None:
        """
        Test creating a new payment transaction with invalid data.
        """
        order = create_order()

        # Attempt to create a transaction with invalid data
        with pytest.raises(IntegrityError):
            PaymeTransactions.objects.create(
                transaction_id=None,
                account=order,
                amount=-100.00,
                state=PaymeTransactions.CREATED
            )

        # Verify that the transaction is not saved in the database
        with pytest.raises(PaymeTransactions.DoesNotExist):
            PaymeTransactions.objects.get(transaction_id=None)

        # Attempt to retrieve the non-existent transaction
        with pytest.raises(PaymeTransactions.DoesNotExist):
            PaymeTransactions.objects.get(transaction_id="invalid_id")

        # Attempt to update a non-existent transaction
        with pytest.raises(PaymeTransactions.DoesNotExist):
            transaction = PaymeTransactions.objects.get(transaction_id="invalid_id")
            transaction.amount = 200.00
            transaction.save()

        # Attempt to delete a non-existent transaction
        with pytest.raises(PaymeTransactions.DoesNotExist):
            transaction = PaymeTransactions.objects.get(transaction_id="invalid_id")
            transaction.delete()
    
    @pytest.mark.django_db(transaction=True)
    def test_create_transaction_with_duplicate_id(self) -> None:
        """
        Test creating a transaction with a duplicate transaction ID.
        """
        order = create_order()
        
        # Create the first transaction
        transaction1 = create_transaction(order)
        assert transaction1.transaction_id == "12345"
        
        # Attempt to create a second transaction with the same ID
        with pytest.raises(IntegrityError):
            create_transaction(order, id="12345")
        
        # Verify that the first transaction is saved in the database
        retrieved_transaction1 = PaymeTransactions.objects.get(transaction_id="12345")
        assert retrieved_transaction1 == transaction1
        
        # Ensure that the second transaction is not saved in the database
        with pytest.raises(PaymeTransactions.DoesNotExist):
            PaymeTransactions.objects.get(transaction_id="12345", id__gt=transaction1.id)
        
        # Verify that the first transaction can be updated
        transaction1.amount = 200.00
        transaction1.save()
        updated_transaction1 = PaymeTransactions.objects.get(transaction_id="12345")
        assert updated_transaction1.amount == 200.00
        
        # Ensure that the second transaction cannot be updated
        with pytest.raises(PaymeTransactions.DoesNotExist):
            transaction2 = PaymeTransactions.objects.get(transaction_id="12345", id__gt=transaction1.id)
            transaction2.amount = 300.00
            transaction2.save()
        
        # Confirm that the first transaction can be deleted
        transaction1.delete()
        with pytest.raises(PaymeTransactions.DoesNotExist):
            PaymeTransactions.objects.get(transaction_id="12345")
        
        # Ensure that the second transaction cannot be deleted
        with pytest.raises(PaymeTransactions.DoesNotExist):
            PaymeTransactions.objects.get(transaction_id="12345", id__gt=updated_transaction1.id)