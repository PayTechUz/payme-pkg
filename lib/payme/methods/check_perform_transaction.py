from payme.models import PaymeOrder as Order
from payme.serializers import MerchatTransactionsModelSerializer
from payme.utils.get_params import clean_empty, get_params


class CheckPerformTransaction:
    """
    CheckPerformTransaction class
    That's used to check perform transaction.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/checktransaction
    """

    def __call__(self, params: dict) -> dict:
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)

        order = Order.objects.get(
            pk=serializer.validated_data.get('order_id')
        )
        detail = clean_empty(order.to_detail())

        response = {
            "result": {
                "allow": True,
                "detail": detail
            }
        }

        return None, response
