from django.db import models
from django.db.models import Case, F, Sum, When


class MerchantTransactionsModel(models.Model):
    """
    MerchantTransactionsModel class \
        That's used for managing transactions in database.
    """
    _id = models.CharField(max_length=255, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=False)
    order_id = models.BigIntegerField(null=True, blank=True)
    amount = models.BigIntegerField(null=True, blank=True)
    time = models.BigIntegerField(null=True, blank=True)
    perform_time = models.BigIntegerField(null=True, default=0)
    cancel_time = models.BigIntegerField(null=True, default=0)
    state = models.IntegerField(null=True, default=1)
    reason = models.CharField(max_length=255, null=True, blank=True)
    created_at_ms = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self._id)

    class Meta:
        # pylint: disable=missing-class-docstring
        verbose_name = "Merchant Transaction"
        verbose_name_plural = "Merchant Transactions"


class ShippingDetail(models.Model):
    """
    ShippingDetail class \
        That's used for managing shipping
    """
    title = models.CharField(max_length=255)
    price = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        shipping_price = self.price / 100  # shipping price in soum
        return f"[{self.pk}] {self.title} - {shipping_price:,}"

    class Meta:
        # pylint: disable=missing-class-docstring
        verbose_name = "Shipping Detail"
        verbose_name_plural = "Shipping Details"


class FiscalData(models.Model):
    """
    FiscalData class \
        That's used for managing fiscalization items
    """
    code = models.CharField(max_length=17)
    units = models.IntegerField(null=True, blank=True)
    package_code = models.CharField(max_length=255)
    vat_percent = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.code} - {self.package_code}"

    class Meta:
        # pylint: disable=missing-class-docstring
        verbose_name = "Fiscal Data"
        verbose_name_plural = "Fiscal Data"


class Item(models.Model):
    """
    Item class \
        That's used for managing order items
    """
    discount = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    price = models.BigIntegerField(default=0)
    count = models.IntegerField(default=1)
    fiscal_data = models.ForeignKey(
        FiscalData, null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        item_price = self.price / 100  # item price in soum
        return f"[{self.pk}] {self.title} ({self.count} pc.) x {item_price:,} UZS"

    class Meta:
        # pylint: disable=missing-class-docstring
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"


class DisallowOverrideMetaclass(models.base.ModelBase):
    # pylint: disable=missing-class-docstring
    def __new__(mcs, name, bases, attrs: dict, **kwargs):
        disallowed_fields = ['amount', 'receipt_type', 'shipping']

        if name != 'BaseOrder':
            for field_name in disallowed_fields:
                if not attrs.get(field_name):
                    continue

                raise TypeError(
                    f"Field '{field_name}' in '{name}' cannot be overridden."
                )

        return super().__new__(mcs, name, bases, attrs, **kwargs)


class BaseOrder(models.Model, metaclass=DisallowOverrideMetaclass):
    """
    Order class \
        That's used for managing order process
    """
    receipt_type = models.IntegerField(default=0)
    items = models.ManyToManyField(Item)
    shipping = models.ForeignKey(
        to=ShippingDetail,
        null=True, blank=True,
        on_delete=models.CASCADE
    )

    @property
    def amount(self) -> int:
        # pylint: disable=missing-function-docstring
        items = self.items.all().aggregate(
            total_price=Sum(
                Case(
                    When(discount__isnull=True, then=F('price') * F('count')),
                    default=(F('price') * F('count')) - F('discount'),
                    output_field=models.BigIntegerField()
                )
            )
        )
        shipping_price = self.shipping.price if self.shipping else 0
        return int(shipping_price + items['total_price']) / 100

    def __str__(self):
        return f"ORDER ID: {self.pk} - AMOUNT: {self.amount:,} UZS"

    class Meta:
        # pylint: disable=missing-class-docstring
        abstract = True
        verbose_name = "Order"
        verbose_name_plural = "Orders"
