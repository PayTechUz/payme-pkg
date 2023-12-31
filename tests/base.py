import json
import logging
from unittest import TestCase

from environs import Env

from lib.payme.cards.subscribe_cards import PaymeSubscribeCards
from lib.payme.receipts.subscribe_receipts import PaymeSubscribeReceipts

env = Env()
env.read_env()


class BaseTestCase(TestCase):
    # pylint: disable=missing-class-docstring
    base_url = env.str("PAYCOM_BASE_URL")
    paycom_id = env.str("PAYCOM_ID")
    paycom_key = env.str("PAYCOM_KEY")

    card_number = "8600069195406311"
    card_expire = "0399"

    fixture_file_path = "tests/fixtures/data.json"

    def update_data(self, token: str = None, invoice_id: str = None) -> None:
        with open(self.fixture_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        data["token"] = token if token or token == "" else data["token"]
        data["invoice_id"] = invoice_id if invoice_id or invoice_id == "" else data["invoice_id"]

        with open(self.fixture_file_path, "w", encoding="utf-8")as file:
            json.dump(data, file, indent=2)

    def get_data(self) -> dict:
        with open(self.fixture_file_path, "r", encoding="utf-8") as data:
            return json.load(data)

    def _test_cards_create(self) -> None:
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

        self.update_data(token=card["token"])

    def _test_cards_verify(self) -> None:
        response = self.subscribe_client.card_get_verify_code(
            token=self.get_data()["token"])
        self.assertTrue(response["result"]["sent"])
        self.assertEqual(response["result"]["phone"], "99890*****66")

        response = self.subscribe_client.cards_verify(
            verify_code="666666",
            token=self.get_data()["token"],
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
