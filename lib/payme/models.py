from django.db import models


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


class PaymeItem(models.Model):
    """
    Item class \
        That's used for managing order items
    """

    discount = models.BigIntegerField(default=0)
    title = models.CharField(max_length=255)
    price = models.BigIntegerField(default=0)
    fiscal_data = models.ForeignKey(FiscalData, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        item_price = self.price / 100  # item price in soum
        return f"[{self.pk}] {self.title} {item_price:,} UZS"

    class Meta:
        # pylint: disable=missing-class-docstring
        verbose_name = "Payme Item"
        verbose_name_plural = "Payme Items"


class PaymeOrder(models.Model):
    """
    Order class \
        That's used for managing order process
    """

    receipt_type = models.IntegerField(default=0)
    shipping = models.ForeignKey(
        to=ShippingDetail, null=True, blank=True, on_delete=models.CASCADE
    )

    @property
    def amount(self) -> int:
        shipping_price = self.shipping.price if self.shipping else 0
        return int(shipping_price + self.cart_total) / 100

    @property
    def cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.price for item in orderitems)
        return total

    @property
    def cart_items(self):
        orderitems = self.orderitem_set.all()
        total_count = sum(item.count for item in orderitems)
        return total_count

    def to_detail(self):
        orderitems = self.orderitem_set.all()
        return {
            "receipt_type": self.receipt_type,
            "shipping": {"title": self.shipping.title, "price": self.shipping.price}
            if self.shipping
            else None,
            "items": [item.item_as_dict for item in orderitems],
        }

    def __str__(self):
        return f"ORDER ID: {self.pk} - AMOUNT: {self.amount:,} UZS"

    class Meta:
        # pylint: disable=missing-class-docstring
        verbose_name = "Payme Order"
        verbose_name_plural = "Payme Orders"


class OrderItem(models.Model):
    """
    Order Item class \
        That's used for managing order items process
    """

    item = models.ForeignKey(PaymeItem, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(PaymeOrder, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(default=1)

    @property
    def price(self):
        return (self.item.price * self.count) - (self.item.discount * self.count)

    @property
    def item_as_dict(self):
        fiscal_data = (
            {
                "code": self.item.fiscal_data.code,
                "units": self.item.fiscal_data.units,
                "package_code": self.item.fiscal_data.package_code,
                "vat_percent": self.item.fiscal_data.vat_percent,
            }
            if self.item.fiscal_data
            else {}
        )

        return {
            "discount": self.item.discount,
            "title": self.item.title,
            "count": self.count,
            "price": self.item.price,
            "code": fiscal_data.get("code"),
            "units": fiscal_data.get("units"),
            "package_code": fiscal_data.get("package_code"),
            "vat_percent": fiscal_data.get("vat_percent"),
        }

    def __str__(self):
        return f"ORDER ID: {self.order.pk} | ITEM: {self.item.title}"

    class Meta:
        # pylint: disable=missing-class-docstring
        verbose_name = "Payme Order Item"
        verbose_name_plural = "Payme Order Items"
