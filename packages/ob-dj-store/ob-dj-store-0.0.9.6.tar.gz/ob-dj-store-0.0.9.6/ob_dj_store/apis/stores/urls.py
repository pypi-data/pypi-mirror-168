from django.conf.urls import include
from django.urls import path
from rest_framework_nested import routers

from ob_dj_store.apis.stores.views import (
    CartItemView,
    CartView,
    CategoryViewSet,
    InventoryView,
    OrderView,
    PaymentMethodViewSet,
    ProductView,
    ShippingMethodViewSet,
    StoreView,
    TaxViewSet,
    TransactionsViewSet,
    VariantView,
)

app_name = "stores"

router = routers.SimpleRouter()
router.register(r"stores", StoreView)

stores_router = routers.NestedSimpleRouter(router, r"stores", lookup="store")
stores_router.register(r"order", OrderView, basename="order")
stores_router.register(r"product", ProductView, basename="product")
stores_router.register(r"variant", VariantView, basename="variant")
stores_router.register(r"inventory", InventoryView, basename="inventory")
stores_router.register(
    r"payment-method", PaymentMethodViewSet, basename="payment-method"
)
router.register(r"shipping-method", ShippingMethodViewSet, basename="shipping-method")
router.register(r"tax", TaxViewSet, basename="tax")
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"transaction", TransactionsViewSet, basename="transaction")
router.register(r"cart", CartView, basename="cart")
router.register(r"cart-item", CartItemView, basename="cart-item")
urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(stores_router.urls)),
]
