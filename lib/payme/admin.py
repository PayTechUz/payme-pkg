from django.contrib import admin

from payme.models import (
    FiscalData, Item, ShippingDetail,
    MerchantTransactionsModel
)

admin.site.register(
    [
        MerchantTransactionsModel,
        FiscalData,
        Item,
        ShippingDetail
    ]
)
