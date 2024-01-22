from unittest import mock
from payme.tests.base import BaseTestCase


class SubscribeCardsTest(BaseTestCase):
    # pylint: disable=missing-class-docstring
    def test_cards_create(self) -> None:
        self._test_cards_create()

    def test_cards_verify(self) -> None:
        self._test_cards_verify()

    def test_cards_check(self) -> None:
        with mock.patch(
            "payme.cards.subscribe_cards.PaymeSubscribeCards.cards_check",
            return_value={"result": {"card": {
                "number": "860006******6311",
                "expire": "03/99",
                "recurrent": True,
                "verify": True,
                "type": "22618",
                "token": "mocked_token"
            }}}
        ):
            response = self.subscribe_client.cards_check("mocked_token")

        card = response["result"]["card"]

        self.assertEqual(card["number"], "860006******6311")
        self.assertEqual(card["expire"], "03/99")
        self.assertTrue(card["recurrent"])
        self.assertTrue(card["verify"])
        self.assertEqual(card["type"], "22618")

    def test_cards_remove(self) -> None:
        with mock.patch(
            "payme.cards.subscribe_cards.PaymeSubscribeCards.cards_remove",
            return_value={"result": {"success": True}}
        ):
            response = self.subscribe_client.cards_remove("mocked_token")

        self.assertTrue(response["result"]["success"])
