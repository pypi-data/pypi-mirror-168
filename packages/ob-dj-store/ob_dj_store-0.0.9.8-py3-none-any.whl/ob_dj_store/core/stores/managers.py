import typing

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings


class ActiveMixin:
    def active(self):
        return self.filter(is_active=True)


class StoreManager(ActiveMixin, models.Manager):
    pass


class CategoryManager(ActiveMixin, models.Manager):
    pass


class ProductVariantManager(models.Manager):
    def active(self):
        pass


class ProductManager(ActiveMixin, models.Manager):
    pass


class CartManager(models.Manager):
    pass


class CartItemManager(models.Manager):
    pass


class ShippingMethodManager(ActiveMixin, models.Manager):
    pass


class PaymentMethodManager(ActiveMixin, models.Manager):
    pass


class PaymentManager(models.Manager):
    def create(self, *args: typing.Any, **kwargs: typing.Any):
        from ob_dj_store.core.stores.gateway.tap.models import TapPayment
        from ob_dj_store.core.stores.models import Tax, WalletTransaction

        try:
            kwargs["payment_tax"] = Tax.objects.get(is_active=True)
        except ObjectDoesNotExist:
            raise ValidationError(_("Tax object is missing"), code="invalid")
        gateway = settings.DEAFULT_PAYMENT_METHOD
        method = kwargs.get("method", None)
        if method:
            gateway = method.payment_provider
        instance: "models.Payment" = super().create(*args, **kwargs)
        if gateway in [settings.TAP_CREDIT_CARD, settings.TAP_KNET, settings.TAP_ALL]:
            source = gateway
            TapPayment.objects.create(
                source=source,
                payment=instance,
                user=kwargs.get("user"),
            )
        elif gateway == settings.WALLET:
            WalletTransaction.objects.create(
                wallet=kwargs["user"].wallet,
                type=WalletTransaction.TYPE.DEBIT,
                amount=kwargs["amount"],
            )

        return instance


class InventoryManager(ActiveMixin, models.Manager):
    pass


class OrderManager(models.Manager):
    def create(self, *args, **kwargs):
        order = super().create(**kwargs)
        return order


class FavoriteManager(ActiveMixin, models.Manager):
    def favorites_for_user(self, user):
        """Returns Favorites for a specific user"""
        return self.get_queryset().filter(user=user)

    def favorites_for_model(self, model, user=None):
        """Returns Favorites for a specific model"""
        content_type = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=content_type).only("id")
        if user:
            qs = qs.filter(user=user)
        return qs

    def favorites_for_object(self, obj, user=None):
        """Returns Favorites for a specific object"""
        content_type = ContentType.objects.get_for_model(type(obj))
        qs = self.get_queryset().filter(content_type=content_type, object_id=obj.pk)
        if user:
            qs = qs.filter(user=user)

        return qs

    def favorite_for_user(self, obj, user):
        """Returns the favorite, if exists for obj by user"""
        content_type = ContentType.objects.get_for_model(type(obj))
        return self.get_queryset().get(content_type=content_type, object_id=obj.pk)


class InventoryOperationsManager(ActiveMixin, models.Manager):

    # override create method to set the inventory_quantity
    def create(self, *args, **kwargs):
        from ob_dj_store.core.stores.models._inventory import (
            Inventory,
            InventoryOperations,
        )

        # based on the operation type, set the inventory_quantity
        # get the store and the product variant in the kwargs
        store = kwargs.get("store")
        product_variant = kwargs.get("product_variant")
        # get the inventory_quantity from the product variant
        if inventory := Inventory.objects.filter(
            store=store, variant=product_variant
        ).first():
            inventory_quantity = inventory.quantity
            operation_quantity = kwargs.get("quantity")

            if (
                kwargs.get("type_of_operation")
                == InventoryOperations.Type_of_operation.STOCK_IN
            ):
                inventory_quantity += operation_quantity
            elif (
                kwargs.get("type_of_operation")
                == InventoryOperations.Type_of_operation.STOCK_OUT
            ):
                inventory_quantity -= operation_quantity

            inventory.quantity = inventory_quantity
            inventory.save()

        return super().create(*args, **kwargs)


class FeedbackAttributeManager(models.Manager):
    def create(self, **kwargs):
        if "attribute" in kwargs:
            config = self.model.config.field.related_model.objects.get(
                attribute=kwargs["attribute"]
            )
            del kwargs["attribute"]
            kwargs["config"] = config
        return super().create(**kwargs)


class ProductVariantStoreManager(models.Manager):
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)


class WalletTransactionManager(models.Manager):
    def create(self, *args, **kwargs):
        from ob_dj_store.core.stores.models._wallet import WalletTransaction

        wallet = kwargs["wallet"]
        type = kwargs["type"]
        if type == WalletTransaction.TYPE.DEBIT and wallet.balance < kwargs["amount"]:
            raise ValidationError(_("Insufficient Funds"))
        return super().create(*args, **kwargs)
