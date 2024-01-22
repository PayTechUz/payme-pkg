from unittest import mock
from payme.tests.base import BaseTestCase


class ReceiptsTest(BaseTestCase):
    # pylint: disable=missing-class-docstring
    def assert_receipts_data(self, response) -> None:
        card = response["result"]["receipt"]["card"]

        self.assertEqual(card["expire"], "9903")
        self.assertEqual(card["number"], "860006******6311")
        self.assertEqual(response["result"]["receipt"]["amount"], 10000)
        self.assertEqual(response["result"]["receipt"]["payer"]["phone"], "998901304527")

    def test_cards_create(self) -> None:
        self._test_cards_create()
        self._test_cards_verify()

    def test_receipts_create(self) -> None:
        with mock.patch(
            "payme.receipts.subscribe_receipts.PaymeSubscribeReceipts.receipts_create",
            return_value={"result": {"receipt": {"amount": 10000, "_id": "mocked_invoice_id"}}}
        ):
            response = self.receipts_client.receipts_create(
                amount=10000,
                order_id="1",
            )

        self.assertEqual(response["result"]["receipt"]["amount"], 10000)

    def test_receipts_pay(self) -> None:
        with mock.patch(
            "payme.receipts.subscribe_receipts.PaymeSubscribeReceipts.receipts_pay",
            return_value={
                "result": {
                    "receipt": {
                        "card": {
                            "expire": "9903",
                            "number": "860006******6311"
                        },
                        "amount": 10000,
                        "payer": {
                            "phone": "998901304527"
                        }
                    }
                }
            }
        ):
            response = self.receipts_client.receipts_pay(
                invoice_id="mocked_invoice_id",
                token="mocked_token",
                phone="998901304527",
            )
        self.assert_receipts_data(response)

    def test_receipts_send(self) -> None:
        with mock.patch(
            "payme.receipts.subscribe_receipts.PaymeSubscribeReceipts.receipts_send",
            return_value={"result": {"success": True}}
        ):
            response = self.receipts_client.receipts_send(
                invoice_id="mocked_invoice_id",
                phone="998901304527",
            )
        self.assertTrue(response["result"]["success"])

    def test_receipts_check(self) -> None:
        with mock.patch(
            "payme.receipts.subscribe_receipts.PaymeSubscribeReceipts.receipts_check",
            return_value={"result": {"state": 4}}
        ):
            response = self.receipts_client.receipts_check(
                invoice_id="mocked_invoice_id",
            )
        self.assertEqual(response["result"]["state"], 4)

    def test_receipts_get(self) -> None:
        with mock.patch(
            "payme.receipts.subscribe_receipts.PaymeSubscribeReceipts.receipts_get",
            return_value={
                "result": {
                    "receipt": {
                        "card": {
                            "expire": "9903",
                            "number": "860006******6311"
                        },
                        "amount": 10000,
                        "payer": {
                            "phone": "998901304527"
                        }
                    }
                }
            }
        ):
            response = self.receipts_client.receipts_get(
                invoice_id="mocked_invoice_id",
            )
        self.assert_receipts_data(response)

    def test_receipts_get_all(self) -> None:
        with mock.patch(
            "payme.receipts.subscribe_receipts.PaymeSubscribeReceipts.receipts_get_all",
            return_value={"result": [{"receipt": {"amount": 10000}}, {"receipt": {"amount": 5000}}]}
        ):
            response = self.receipts_client.receipts_get_all(
                count=2,
                _from=1636398000000,
                _to=1636398000000,
                offset=0,
            )
        self.assertEqual(len(response["result"]), 2)

    def test_receipts_cancel(self) -> None:
        with mock.patch(
            "payme.receipts.subscribe_receipts.PaymeSubscribeReceipts.receipts_cancel",
            return_value={"result": {"receipt": {"meta": {"source_cancel": "subscribe"}}}}
        ):
            response = self.receipts_client.receipts_cancel(
                invoice_id="mocked_invoice_id",
            )
        self.assertEqual(response["result"]["receipt"]["meta"]["source_cancel"], "subscribe")
