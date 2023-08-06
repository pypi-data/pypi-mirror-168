import logging
from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from ob_dj_store.core.stores.managers import PaymentManager
from ob_dj_store.core.stores.models import Order

logger = logging.getLogger(__name__)


class Tax(models.Model):
    """
    As a user, I should be able to see tax added to my payment summary of each order.
    Tax should be a model holding "name", "description" and "rate".
    Rate should be one of two types, either percentage or flat, and it should have a value.
    Tax should be calculated with the order total once the order moves to payment process
    """

    class Rates(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", _("percentage")
        FLAT = "FLAT", _("flat")

    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=200, help_text=_("Name"))
    rate = models.CharField(
        max_length=32, choices=Rates.choices, help_text="Tax Rate for the given payment"
    )
    is_applied = models.BooleanField(default=True)
    value = models.DecimalField(
        blank=True,
        max_digits=5,
        decimal_places=4,
        null=True,
        help_text="Value for the given Payment -> 0.0625",
    )
    is_active = models.BooleanField(default=False)
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def value_to_percentage(self) -> Decimal:
        """Converts tax value to percentage
        Args:
            value (Decimal): Value
        Returns:
            Decimal: Tax Value Percentage Example -> 6.2500
        """
        return "{:.2%}".format(self.value)

    def save(self, *args, **kwargs):
        if not self.is_active:
            return super(Tax, self).save(*args, **kwargs)
        with transaction.atomic():
            Tax.objects.filter(is_active=True).update(is_active=False)
            return super(Tax, self).save(*args, **kwargs)


class Payment(models.Model):
    """Payment captures the order payment either COD or via a Gateway"""

    class PaymentStatus(models.TextChoices):
        INIT = "INIT"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        ERROR = "ERROR"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True,
    )
    status = models.CharField(
        max_length=100,
        default=PaymentStatus.INIT,
        choices=PaymentStatus.choices,
    )
    method = models.ForeignKey(
        "stores.PaymentMethod",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    payment_tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
    )
    orders = models.ManyToManyField("stores.Order", related_name="payments")
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    currency = models.CharField(_("Currency"), max_length=10)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    payment_post_at = models.DateTimeField(_("Payment Post At"), null=True, blank=True)

    objects = PaymentManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment (PK={self.pk})"

    def mark_paid(self):
        self.status = self.PaymentStatus.SUCCESS
        orders = list(self.orders.all())
        cart = self.user.cart
        for order in orders:
            order.status = Order.OrderStatus.PAID
            order.save()
            items = order.store.store_items.filter(cart=cart)
            items.delete()
        self.save()

    def mark_failed(self):
        self.status = self.PaymentStatus.FAILED
        self.save()

    @property
    def total_payment(self):
        sum_orders = Decimal(
            sum(map(lambda order: Decimal(order.total_amount) or 0, self.orders.all()))
        )
        if self.payment_tax.rate == Tax.Rates.PERCENTAGE:
            perc = Decimal(sum_orders * self.payment_tax.value / 100)
            return sum_orders + perc

        return sum_orders + Decimal(self.payment_tax.value)

    @property
    def is_digital(self):
        order = list(self.orders.all())[0]
        return order.is_digital
