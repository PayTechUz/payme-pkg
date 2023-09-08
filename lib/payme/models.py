from django.db import models


class MerchatTransactionsModel(models.Model):
    """
    MerchatTransactionsModel class \
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


class ShippingDetail(models.Model):
    """
    ShippingDetail class \
        That's used for managing shipping
    """
    title = models.CharField(max_length=255)
    price = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.title} - {self.price:,}"


class Item(models.Model):
    """
    Item class \
        That's used for managing order items
    """
    discount = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    price = models.BigIntegerField(default=0)
    count = models.IntegerField(default=1)
    code = models.CharField(max_length=17)
    units = models.IntegerField(null=True, blank=True)
    package_code = models.CharField(max_length=255)
    vat_percent = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return f"[{self.id}] {self.title} ({self.count} pc.) x {self.price:,} UZS"


class OrderDetail(models.Model):
    """
    OrderDetail class \
        That's used for managing order details
    """
    receipt_type = models.IntegerField(default=0)
    shipping = models.ForeignKey(
        to=ShippingDetail,
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    items = models.ManyToManyField(Item)

    @property
    def get_items_display(self):
        # pylint: disable=missing-function-docstring
        item_display = [f'[{self.pk}]']

        for fld in self._meta.get_fields():
            if not isinstance(fld, models.ManyToOneRel):
                continue

            if not issubclass(fld.related_model, BaseOrder):
                continue

            related_order = fld.get_accessor_name()
            orders = getattr(self, related_order).values()

            order_id = orders[0].get('id') if orders else 'None'

            item_display.append(f'FOR ORDER - {order_id}')
            if self.shipping: item_display.append(f'ADDRESS: {self.shipping.title}')
            item_display.append(f'AMOUNT: {self.get_total_items_price} UZS')

        return ' '.join(item_display)

    @property
    def get_total_items_price(self) -> int:
        # pylint: disable=missing-function-docstring
        items = self.items.all().aggregate(
            total_price=models.Sum(
                models.Case(
                    models.When(
                        discount__isnull=True,
                        then=models.F('price') * models.F('count')
                    ),
                    default=(
                        (models.F('price') * models.F('count')) -
                        models.F('discount')
                    ),
                    output_field=models.BigIntegerField()
                )
            )
        )
        shipping_price = self.shipping.price if self.shipping else 0
        return f"{shipping_price + items['total_price']:,}"

    def __str__(self) -> str:
        return f"{self.get_items_display}"


class DisallowOverrideMetaclass(models.base.ModelBase):
    # pylint: disable=missing-class-docstring
    def __new__(mcs, name, bases, attrs: dict, **kwargs):
        disallowed_fields = ['amount', 'detail']

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
    detail = models.ForeignKey(
        OrderDetail,
        null=True, blank=True,
        on_delete=models.CASCADE
    )

    @property
    def amount(self):
        # pylint: disable=missing-function-docstring
        return self.detail.get_total_items_price if self.detail else 0

    def __str__(self):
        return f"ORDER ID: {self.id} - AMOUNT: {self.amount} UZS"

    class Meta:
        # pylint: disable=missing-class-docstring
        abstract = True
