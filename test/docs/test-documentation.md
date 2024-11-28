# Test documentation

This is a test documentation file. It contains information about the test cases and the test results.

## Unit tests

1. Test creating a new payment transaction
   - Verify that a new payment transaction can be created with valid data.
2. Test creating a new payment transaction with invalid data
   - Ensure that creating a payment transaction with invalid data raises appropriate errors.
3. Test string representation of the payment transaction
   - Check that the string representation of the payment transaction is formatted correctly.
4. Test `is_performed` method of the payment transaction
   - Confirm that the `is_performed` method returns True if the transaction is successfully performed.
5. Test `is_cancelled` method of the payment transaction
   - Verify that the `is_cancelled` method returns True if the transaction is cancelled.
6. Test `is_created_in_payme` method of the payment transaction
   - Ensure that the `is_created_in_payme` method returns True if the transaction is in the initiating state.
7. Test `mark_as_cancelled` method of the payment transaction
   - Check that the `mark_as_cancelled` method correctly updates the transaction state to cancelled.
8. Test `mark_as_performed` method of the payment transaction
   - Verify that the `mark_as_performed` method correctly updates the transaction state to successfully performed.
9. Test `get_by_transaction_id` method of the payment transaction
   - Ensure that the `get_by_transaction_id` method retrieves the correct transaction by its ID.
10. Test `is_created` method of the payment transaction
    - Verify that the `is_created` method returns True if the transaction is in the created state.
11. Test updating the amount of a payment transaction
    - Check that the amount of a payment transaction can be updated correctly.
12. Test updating the account of a payment transaction
    - Ensure that the account associated with a payment transaction can be updated correctly.
13. Test `updated_at` field of the payment transaction
    - Verify that the `updated_at` field is updated correctly when the transaction is modified.
14. Test `created_at` field of the payment transaction
    - Ensure that the `created_at` field is set correctly when the transaction is created.
15. Test `performed_at` field of the payment transaction
    - Check that the `performed_at` field is set correctly when the transaction is marked as performed.
16. Test `cancelled_at` field of the payment transaction
    - Verify that the `cancelled_at` field is set correctly when the transaction is marked as cancelled.
17. Test creating a transaction with a duplicate transaction ID
    - Ensure that creating a transaction with a duplicate transaction ID raises an error.
18. Test marking a transaction as performed when it is already performed
    - Verify that marking a transaction as performed when it is already performed does not change its state.
19. Test marking a transaction as cancelled when it is already cancelled
    - Ensure that marking a transaction as cancelled when it is already cancelled does not change its state.
20. Test creating a transaction with a negative amount
    - Verify that creating a transaction with a negative amount raises an error.
21. Test creating a transaction with a very large amount
    - Ensure that creating a transaction with a very large amount is handled correctly.
