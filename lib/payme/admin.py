from django.contrib import admin
from payme.models import (
    FiscalData, MerchantTransactionsModel, PaymeItem,
    PaymeOrder, ShippingDetail, OrderItem
)

admin.site.register(
    [
        MerchantTransactionsModel,
        FiscalData,
        PaymeItem,
        PaymeOrder,
        OrderItem,
        ShippingDetail
    ]
)
