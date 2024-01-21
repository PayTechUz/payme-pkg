import logging
from unittest import TestCase, mock

from payme.cards.subscribe_cards import PaymeSubscribeCards
from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts


class BaseTestCase(TestCase):
    # pylint: disable=missing-class-docstring
    base_url = "https://checkout.test.paycom.uz/api"
    paycom_id = "test_paycom_id"
    paycom_key = "test_paycom_key"

    card_number = "8600069195406311"
    card_expire = "0399"

    def _test_cards_create(self) -> None:
        with mock.patch(
            "payme.cards.subscribe_cards.PaymeSubscribeCards.cards_create",
            return_value={"result": {"card": {
                "number": "860006******6311",
                "expire": "03/99",
                "recurrent": True,
                "verify": False,
                "type": "22618",
                "token": "mocked_token"
            }}}
        ):
            response = self.subscribe_client.cards_create(
                self.card_number,
                self.card_expire,
                True,
            )

        card = response["result"]["card"]

        self.assertEqual(card["number"], "860006******6311")
        self.assertEqual(card["expire"], "03/99")
        self.assertTrue(card["recurrent"])
        self.assertFalse(card["verify"])
        self.assertEqual(card["type"], "22618")

    def _test_cards_verify(self) -> None:
        with mock.patch(
            "payme.cards.subscribe_cards.PaymeSubscribeCards.card_get_verify_code",
            return_value={"result": {"sent": True, "phone": "99890*****66"}}
        ):
            response = self.subscribe_client.card_get_verify_code(
                token="mocked_token"
            )
        self.assertTrue(response["result"]["sent"])
        self.assertEqual(response["result"]["phone"], "99890*****66")

        with mock.patch(
            "payme.cards.subscribe_cards.PaymeSubscribeCards.cards_verify",
            return_value={"result": {"card": {"verify": True}}}
        ):
            response = self.subscribe_client.cards_verify(
                verify_code="666666",
                token="mocked_token",
            )

        self.assertTrue(response["result"]["card"]["verify"])

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.disable(logging.CRITICAL)

        cls.subscribe_client = PaymeSubscribeCards(
            base_url=cls.base_url,
            paycom_id=cls.paycom_id,
        )

        cls.receipts_client = PaymeSubscribeReceipts(
            base_url=cls.base_url,
            paycom_id=cls.paycom_id,
            paycom_key=cls.paycom_key,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        logging.disable(logging.NOTSET)
