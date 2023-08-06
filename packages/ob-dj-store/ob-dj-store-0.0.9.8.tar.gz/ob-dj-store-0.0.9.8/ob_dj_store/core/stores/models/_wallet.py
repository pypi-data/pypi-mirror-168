import logging
import typing
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

from ob_dj_store.core.stores.managers import WalletTransactionManager

logger = logging.getLogger(__name__)


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet",
    )

    def __str__(self) -> typing.Text:
        return f"Wallet(PK={self.pk})"

    @property
    def balance(self) -> Decimal:
        from ob_dj_store.core.stores.models import WalletTransaction

        query = self.transactions.aggregate(
            balance=Coalesce(
                models.Sum(
                    "amount", filter=models.Q(type=WalletTransaction.TYPE.CREDIT)
                ),
                models.Value(0),
            )
            - Coalesce(
                models.Sum(
                    "amount", filter=models.Q(type=WalletTransaction.TYPE.DEBIT)
                ),
                models.Value(0),
            )
        )
        return query["balance"]


class WalletTransaction(models.Model):
    """

    As a user, I should be able to view my wallet transactions (debit/credit).
    WalletTransaction type should be one of two types, either debit or credit.

    """

    class TYPE(models.TextChoices):
        CREDIT = "CREDIT", _("credit")
        DEBIT = "DEBIT", _("debit")

    wallet = models.ForeignKey(
        "stores.Wallet",
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    type = models.CharField(
        max_length=100,
        choices=TYPE.choices,
    )

    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    currency = models.CharField(
        _("Currency"),
        max_length=10,
        null=True,
        blank=True,
    )

    objects = WalletTransactionManager()

    # Audit
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return f"WalletTransaction (PK={self.pk})"
