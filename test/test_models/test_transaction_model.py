import unittest

from payme.models import Transaction

class TestTransactionModel(unittest.TestCase):
    def test_transaction_model(self):
        transaction = Transaction(
            amount=100,
            currency='USD',
            status='pending'
        )
        self.assertEqual(transaction.amount, 100)
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.status, 'pending')



if __name__ == '__main__':
    unittest.main()