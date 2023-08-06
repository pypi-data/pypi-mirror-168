from django import forms
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from ob_dj_store.core.stores import models


class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "shipping_fee_option",
        "shipping_fee",
        "is_active",
    ]
    search_fields = [
        "name",
    ]
    list_filter = [
        "shipping_fee_option",
        "is_active",
    ]


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "payment_provider",
        "is_active",
    ]
    search_fields = [
        "name",
    ]
    list_filter = ["payment_provider", "is_active"]


class StoreAdmin(LeafletGeoAdmin):
    list_display = [
        "name",
        "location",
        "is_active",
        "currency",
        "minimum_order_amount",
        "delivery_charges",
        "min_free_delivery_amount",
    ]
    # define the pickup addresses field as a ManyToManyField
    # to the address model
    filter_horizontal = ["pickup_addresses"]
    # define the shipping methods field as a ManyToManyField
    # to the shipping method model
    filter_horizontal = ["shipping_methods"]
    search_fields = ["name", "address"]
    list_filter = ("is_active",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "location",
                    "address",
                    "is_active",
                    "poly",
                    "currency",
                    "minimum_order_amount",
                    "payment_methods",
                    "pickup_addresses",
                )
            },
        ),
        (
            "shipping info",
            {
                "fields": (
                    "shipping_methods",
                    "delivery_charges",
                    "min_free_delivery_amount",
                )
            },
        ),
    )


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = [
        "store",
        "from_hour",
        "to_hour",
    ]
    search_fields = [
        "store__name",
    ]
    list_filter = [
        "weekday",
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "parent", "image"]
    search_fields = [
        "name",
        "parent__name",
    ]
    list_filter = [
        "is_active",
    ]


class AttributeChoiceInlineAdmin(admin.TabularInline):
    model = models.AttributeChoice


class ProductVariantInlineAdmin(admin.TabularInline):
    model = models.ProductVariant
    extra = 1


class ProductMediaInlineAdmin(admin.TabularInline):
    model = models.ProductMedia
    extra = 1


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "product",
        "has_inventory",
    ]
    list_filter = [
        "has_inventory",
    ]
    search_fields = [
        "name",
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "category",
    ]
    inlines = [ProductVariantInlineAdmin, ProductMediaInlineAdmin]
    list_filter = ["type", "is_active"]
    search_fields = ["name", "category__name"]


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "type", "is_mandatory"]
    search_fields = [
        "name",
    ]
    list_filter = ["is_mandatory", "type"]


class AttributeChoiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description"]
    search_fields = [
        "name",
    ]


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = [
        "name",
    ]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.base_fields["text_color"].widget = forms.TextInput(attrs={"type": "color"})
        form.base_fields["background_color"].widget = forms.TextInput(
            attrs={"type": "color"}
        )
        return form


class CartItemInlineAdmin(admin.TabularInline):
    readonly_fields = [
        "unit_price",
    ]
    list_display = [
        "product_variant",
        "quantity",
    ]
    model = models.CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ["customer", "total_price"]
    inlines = [CartItemInlineAdmin]
    search_fields = [
        "customer__email",
    ]


class AdressAdmin(LeafletGeoAdmin):
    list_display = [
        "id",
        "address_line",
        "postal_code",
        "city",
        "region",
        "country",
        "is_active",
    ]
    search_fields = [
        "address_line",
        "city",
        "region",
        "country",
    ]
    list_filter = [
        "is_active",
    ]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "order",
        "review",
        "notes",
    ]
    list_filter = [
        "review",
    ]
    search_fields = [
        "user__email",
    ]


class FeedbackAttributeAdmin(admin.ModelAdmin):
    list_display = [
        "feedback",
        "config",
        "value",
        "review",
    ]


class FeedbackConfigAdmin(admin.ModelAdmin):
    list_display = [
        "attribute",
        "attribute_label",
        "values",
    ]


class PhoneContactAdmin(admin.ModelAdmin):
    list_display = [
        "phone_number",
        "store",
    ]
    search_fields = ["phone_number", "store__name"]
    list_filter = [
        "is_active",
    ]


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    fields = (
        "product_variant",
        "quantity",
        "unit_value",
        "total_amount",
    )
    readonly_fields = (
        "unit_value",
        "total_amount",
    )

    def unit_value(self, obj):
        return obj.product_variant.price if obj.product_variant else None


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "status",
        "payment_method",
        "store",
        "total_amount",
        "pickup_time",
    ]
    inlines = [OrderItemInline]
    search_fields = [
        "customer__email",
    ]
    date_hierarchy = "created_at"
    list_filter = [
        "payment_method",
        "shipping_method",
        "store",
        "status",
    ]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "method", "amount", "currency", "status")
    list_filter = [
        "method__payment_provider",
        "status",
    ]
    search_fields = [
        "orders",
    ]


class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "variant",
        "store",
        "quantity",
        "is_active",
        "price",
        "discount_percent",
        "is_deliverable",
        "is_primary",
        "is_uncountable",
        "preparation_time",
    ]
    list_filter = [
        "is_deliverable",
        "is_primary",
        "is_uncountable",
    ]


class InventoryOperationsAdmin(admin.ModelAdmin):
    list_display = [
        "inventory",
        "product_variant",
        "type_of_operation",
        "store",
        "operator",
    ]
    list_filter = [
        "type_of_operation",
    ]


class TaxAdmin(admin.ModelAdmin):
    list_display = [
        "value",
        "rate",
        "is_applied",
        "value",
        "name",
        "is_active",
    ]
    list_filter = [
        "is_applied",
        "is_active",
        "rate",
    ]


class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "wallet",
        "type",
        "amount",
        "currency",
    ]
    list_filter = [
        "type",
    ]
    search_fields = [
        "user",
    ]


class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance")
    search_fields = [
        "user__email",
    ]


admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.OpeningHours, OpeningHoursAdmin)
admin.site.register(models.ShippingMethod, ShippingMethodAdmin)
admin.site.register(models.PaymentMethod, PaymentMethodAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductAttribute, ProductAttributeAdmin)
admin.site.register(models.ProductVariant, ProductVariantAdmin)
admin.site.register(models.ProductTag, ProductTagAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Address, AdressAdmin)
admin.site.register(models.Feedback, FeedbackAdmin)
admin.site.register(models.FeedbackAttribute, FeedbackAttributeAdmin)
admin.site.register(models.FeedbackConfig, FeedbackConfigAdmin)
admin.site.register(models.AttributeChoice, AttributeChoiceAdmin)
admin.site.register(models.PhoneContact, PhoneContactAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.InventoryOperations, InventoryOperationsAdmin)
admin.site.register(models.Tax, TaxAdmin)
admin.site.register(models.WalletTransaction, WalletTransactionAdmin)
admin.site.register(models.Wallet, WalletAdmin)
