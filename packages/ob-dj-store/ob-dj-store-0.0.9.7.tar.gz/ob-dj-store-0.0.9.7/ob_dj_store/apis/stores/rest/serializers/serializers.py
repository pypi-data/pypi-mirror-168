import contextlib
import typing
from datetime import date

from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ob_dj_store.core.stores.models import (
    Attribute,
    AttributeChoice,
    Cart,
    CartItem,
    Category,
    Favorite,
    Feedback,
    FeedbackAttribute,
    FeedbackConfig,
    OpeningHours,
    Order,
    OrderHistory,
    OrderItem,
    Payment,
    PaymentMethod,
    PhoneContact,
    Product,
    ProductAttribute,
    ProductMedia,
    ProductTag,
    ProductVariant,
    ShippingMethod,
    Store,
    Tax,
)
from ob_dj_store.core.stores.models._inventory import Inventory
from ob_dj_store.core.stores.utils import distance


class AttributeChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeChoice
        fields = (
            "id",
            "name",
            "price",
        )


class AttributeSerializer(serializers.ModelSerializer):
    attribute_choices = AttributeChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = (
            "id",
            "name",
            "attribute_choices",
        )


class InventoryValidationMixin:
    def validate(self, attrs: typing.Dict) -> typing.Dict:
        validated_data = super().validate(attrs)
        if (
            validated_data["product_variant"].has_inventory
            and validated_data["quantity"] < 1
        ):
            raise serializers.ValidationError(_("Quantity must be greater than 0."))
        # validate quantity in inventory
        stock_quantity = (
            validated_data["product_variant"]
            .inventories.get(store=validated_data["store"])
            .quantity
        )
        if (
            validated_data["product_variant"].has_inventory
            and validated_data["quantity"] > stock_quantity
        ):
            raise serializers.ValidationError(
                _("Quantity is greater than the stock quantity.")
            )
        return validated_data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "description", "is_active")


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = "__all__"


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = "__all__"


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = (
            "id",
            "order",
            "status",
            "created_at",
        )


class OrderItemSerializer(InventoryValidationMixin, serializers.ModelSerializer):
    store = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_variant",
            "quantity",
            "store",
            "total_amount",
            "preparation_time",
            "notes",
            "extra_infos",
            "attribute_choices",
            "attribute_choices_total_amount",
        )

    def create(self, validated_data):
        validated_data.pop("store")
        return super().create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["attribute_choices"] = AttributeChoiceSerializer(
            instance.attribute_choices.all(), many=True
        ).data

        return representation


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    history = OrderHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "store",
            "shipping_method",
            "payment_method",
            "shipping_address",
            "customer",
            "status",
            "items",
            "total_amount",
            "preparation_time",
            "history",
            "pickup_time",
            "extra_infos",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "customer": {"read_only": True},
            "store": {"read_only": True, "required": False},
        }

    def validate(self, attrs):
        # The Cart items must not be empty
        user = self.context["request"].user
        if not user.cart.items.exists():
            raise serializers.ValidationError(_("The Cart must not be empty"))

        """if "pickup_time" in attrs:
            # validate that the pickup_time is always in the future
            if attrs["pickup_time"] < now():
                raise serializers.ValidationError(
                    _("Pickup time must be in the future")
                )
            # validate that the pickup_time is part of day (between 00:00 and 23:59)
            if not (
                attrs["pickup_time"].time() >= time(hour=0, minute=0)
                and attrs["pickup_time"].time() <= time(hour=23, minute=59)
            ):
                raise serializers.ValidationError(_("Pickup time must be part of day"))
            # validate that the pickup_time is between store's opening hours and closing hours
            if (
                attrs["store"]
                .opening_hours.filter(weekday=attrs["pickup_time"].weekday())
                .exists()
            ) and (
                attrs["pickup_time"].hour
                > (
                    attrs["store"]
                    .opening_hours.filter(weekday=attrs["pickup_time"].weekday())
                    .first()
                    .to_hour.hour
                )
                or attrs["pickup_time"].hour
                < (
                    attrs["store"]
                    .opening_hours.filter(weekday=attrs["pickup_time"].weekday())
                    .first()
                    .from_hour.hour
                )
            ):
                raise serializers.ValidationError(
                    _("Pickup time must be between store's opening hours")
                )"""

        return super().validate(attrs)

    def create(self, validated_data: typing.Dict):
        user = self.context["request"].user
        cart = user.cart
        amount = cart.total_price
        stores = Store.objects.filter(store_items__cart=cart)
        orders = []
        for store in stores:
            order = Order.objects.create(
                store=store, customer=cart.customer, **validated_data
            )
            items = store.store_items.filter(cart=cart)
            for item in items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product_variant=item.product_variant,
                    quantity=item.quantity,
                )
                order_item.attribute_choices.set(item.attribute_choices.all())
            orders.append(order)
        digital_items = cart.items.filter(store__isnull=True)
        order = Order.objects.create(customer=cart.customer, **validated_data)
        for item in digital_items:
            order_item = OrderItem.objects.create(
                order=order,
                product_variant=item.product_variant,
                quantity=item.quantity,
                extra_infos=item.extra_infos,
            )
            order_item.attribute_choices.set(item.attribute_choices.all())
            orders.append(order)
        payment = self.init_payment(
            amount=amount,
            method=validated_data.get("payment_method"),
            currency=settings.DEFAULT_CURRENCY,
        )
        payment.orders.set(orders)
        tap_payment = getattr(payment, "tap_payment", None)
        payment_url = None
        if tap_payment:
            payment_url = tap_payment.payment_url
        return {
            "orders": orders,
            "payment_url": payment_url,
        }

    def init_payment(self, amount, method, currency):
        user = self.context["request"].user
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            method=method,
            currency=currency,
        )
        return payment

    def update(self, instance: Order, validated_data: typing.Dict):
        payment_method = validated_data["payment_method"]
        store = instance.store
        if payment_method not in store.payment_methods.all():
            raise serializers.ValidationError(
                _(f"this payment method is not supported")
            )
        return instance


class CreateOrderResponseSerializer(serializers.Serializer):
    orders = OrderSerializer(many=True, read_only=True)
    payment_url = serializers.CharField(read_only=True)
    extra_infos = serializers.JSONField(required=False)

    # write only fields
    shipping_method = serializers.IntegerField(write_only=True, required=False)
    payment_method = serializers.IntegerField(write_only=True, required=False)
    shipping_address = serializers.IntegerField(write_only=True, required=False)
    pickup_time = serializers.DateTimeField(write_only=True, required=False)


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = (
            "id",
            "name",
            "text_color",
            "background_color",
        )


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute_choices = AttributeChoiceSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = (
            "id",
            "name",
            "is_mandatory",
            "attribute_choices",
        )


class ProductVariantSerializer(serializers.ModelSerializer):
    product_attributes = ProductAttributeSerializer(many=True)
    is_primary = serializers.SerializerMethodField()
    active_inventories = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "name",
            "sku",
            "product_attributes",
            "is_primary",
            "active_inventories",
        )

    def get_is_primary(self, obj):
        return True if obj.inventories.filter(is_primary=True).exists() else False

    def get_active_inventories(self, obj):
        if obj.inventories.filter(is_active=True).exists():
            return obj.inventories.filter(is_active=True).values(
                "price", "store", "discount_percent"
            )


class CartItemSerializer(InventoryValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            "id",
            "product_variant",
            "quantity",
            "store",
            "unit_price",
            "total_price",
            "notes",
            "attribute_choices",
            "extra_infos",
            "attribute_choices_total_price",
        )

    def validate(self, attrs: typing.Dict) -> typing.Dict:
        """
        When creating a Cartitem for physical product variant, we create an instance with the fields (product_variant,quantity, notes,store)
        so in case of digital product variant we need to add json field e.g: extra_infos containing the base infos of the giftee.
        """
        if "product_variant" in attrs:
            if attrs[
                "product_variant"
            ].product.type == Product.ProductTypes.PHYSICAL and attrs.get(
                "extra_infos"
            ):
                raise serializers.ValidationError(
                    _("You must not fill extra infos for physical products.")
                )
            if attrs["product_variant"].product.type == Product.ProductTypes.DIGITAL:
                errors = []
                data = attrs.get("extra_infos")
                if not data:
                    raise serializers.ValidationError(
                        f"The Item should include : {' ,'.join(settings.DIGITAL_PRODUCTS_REQUIRED_KEYS)} at least"
                    )
                for key in settings.DIGITAL_PRODUCTS_REQUIRED_KEYS:
                    if not (key in data.keys() and len(str(data.get(key)))):
                        errors.append({key: "This field should be filled."})
                if len(errors) > 0:
                    raise serializers.ValidationError(errors)
        return super(CartItemSerializer, self).validate(attrs)

    def to_representation(self, instance: CartItem):
        data = super().to_representation(instance)
        data["product_variant"] = ProductVariantSerializer(
            instance=instance.product_variant
        ).data
        data["product_name"] = instance.product_variant.product.name
        data["attribute_choices"] = AttributeChoiceSerializer(
            instance.attribute_choices.all(),
            many=True,
        ).data
        return data

    def create(self, validated_data):
        return super().create(**validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            "customer",
            "items",
            "total_price",
            "tax_amount",
            "total_price_with_tax",
        )
        read_only_fields = (
            "id",
            "total_price",
            "tax_amount",
            "total_price_with_tax",
        )

    def update(self, instance, validated_data):
        instance.items.all().delete()
        # update or create instance items
        for item in validated_data["items"]:
            attribute_choices = item.pop("attribute_choices", None)
            cart_item = CartItem.objects.create(
                cart=instance,
                **item,
            )
            if attribute_choices:
                cart_item.attribute_choices.set(attribute_choices)
            cart_item.save()
        return instance


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = (
            "id",
            "is_primary",
            "image",
            "order_value",
        )


class ProductSerializer(serializers.ModelSerializer):
    product_variants = ProductVariantSerializer(many=True)
    product_images = ProductMediaSerializer(many=True, source="images")
    is_favorite = serializers.SerializerMethodField()
    default_variant = ProductVariantSerializer(read_only=True, many=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_favorite",
            "product_images",
            "product_variants",
            "default_variant",
        )

    def get_is_favorite(self, obj):
        if user := self.context["request"].user:
            # The context manager slightly shortens the code and significantly clarifies the author's intention to ignore the specific errors.
            # The standard library feature was introduced following a [discussion](https://bugs.python.org/issue15806), where the consensus was that
            # A key benefit here is in the priming effect for readers...
            # The with statement form makes it clear before you start reading the code that certain exceptions won't propagate.
            # https://docs.python.org/3/library/contextlib.html
            with contextlib.suppress(Favorite.DoesNotExist):
                Favorite.objects.favorite_for_user(obj, user)
                return True
        return False

    def to_representation(self, instance: Product):
        data = super().to_representation(instance=instance)
        return data


class ProductListSerializer(ProductSerializer):
    product_variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "product_images",
            "product_variants",
            "default_variant",
        )


class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "description", "is_active", "products")


class CategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "products",
            "is_active",
            "subcategories",
            "parent",
        )


class FeedbackConfigSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    attribute = serializers.CharField(read_only=True)

    class Meta:
        model = FeedbackConfig
        fields = ("id", "attribute", "attribute_label", "values")


class FeedbackAttributeSerializer(serializers.ModelSerializer):
    config = FeedbackConfigSerializer(many=False, read_only=True)
    attribute = serializers.CharField(write_only=True)

    class Meta:
        model = FeedbackAttribute
        fields = ("attribute", "config", "value", "review")

    # TODO: do we need validations when creating the value


class FeedbackSerializer(serializers.ModelSerializer):
    attributes = FeedbackAttributeSerializer(many=True, required=False)

    class Meta:
        model = Feedback
        fields = (
            "id",
            "attributes",
            "notes",
            "review",
        )

    def validate(self, attrs: typing.Dict):
        # Validate Order Status
        if self.instance.status not in [
            Order.OrderStatus.PAID,
            Order.OrderStatus.CANCELLED,
        ]:
            raise serializers.ValidationError(
                _("The Order must be PAID or CANCELLED to give a feedback")
            )
        return attrs

    def update(self, instance: Order, validated_data: typing.Dict):
        user = self.context["request"].user
        attributes = validated_data.pop("attributes", [])
        feedback = Feedback.objects.create(
            order=self.instance, user=user, **validated_data
        )

        for attr in attributes:
            feedback.attributes.create(**attr)
        feedback.order.save()
        return feedback


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = (
            "id",
            "variant",
            "store",
            "quantity",
            "price",
            "preparation_time",
            "discount_percent",
            "discounted_price",
            "is_primary",
        )

    def to_representation(self, instance):
        data = super(InventorySerializer, self).to_representation(instance)
        data["variant"] = ProductVariantSerializer(instance=instance.variant).data
        return data


class PhoneContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneContact
        fields = (
            "id",
            "phone_number",
            "is_default",
            "is_active",
        )


class StoreSerializer(serializers.ModelSerializer):

    opening_hours = OpeningHourSerializer(many=True, read_only=True)
    phone_contacts = serializers.SerializerMethodField()
    in_range_delivery = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    address_line = serializers.SerializerMethodField()
    shipping_methods = ShippingMethodSerializer(many=True, read_only=True)
    distance = serializers.SerializerMethodField()
    inventories = InventorySerializer(many=True, read_only=True, required=False)
    current_day_opening_hours = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "address",
            "address_line",
            "location",
            "distance",
            "is_active",
            "currency",
            "minimum_order_amount",
            "delivery_charges",
            "shipping_methods",
            "min_free_delivery_amount",
            "opening_hours",
            "in_range_delivery",
            "is_favorite",
            "created_at",
            "updated_at",
            "inventories",
            "phone_contacts",
            "current_day_opening_hours",
        )

    def get_in_range_delivery(self, obj):
        user_location = self.context["request"].query_params.get("point")
        if user_location and obj.poly:
            long, lat = user_location.split(",")
            return obj.poly.contains(Point(float(long), float(lat)))
        return False

    def get_is_favorite(self, obj):
        if user := self.context["request"].user:
            # The context manager slightly shortens the code and significantly clarifies the author's intention to ignore the specific errors.
            # The standard library feature was introduced following a [discussion](https://bugs.python.org/issue15806), where the consensus was that
            # A key benefit here is in the priming effect for readers...
            # The with statement form makes it clear before you start reading the code that certain exceptions won't propagate.
            # https://docs.python.org/3/library/contextlib.html
            with contextlib.suppress(Favorite.DoesNotExist):
                Favorite.objects.favorite_for_user(obj, user)
                return True
        return False

    def get_address_line(self, obj):
        return obj.address.address_line

    def get_distance(self, obj):
        # get the distance between the user location and store location
        user_location = self.context["request"].query_params.get("point")
        if user_location and obj.location:

            lat, long = user_location.split(",")
            store_lat, store_long = obj.location.x, obj.location.y
            return round(
                distance((float(lat), float(long)), (store_lat, store_long)), 1
            )

    def get_phone_contacts(self, obj):
        phone_contacts = obj.phone_contacts.filter(is_active=True).order_by(
            "-is_default"
        )
        return PhoneContactSerializer(phone_contacts, many=True).data

    def get_current_day_opening_hours(self, obj):
        for op_hour in obj.opening_hours.all().only("id"):
            if op_hour.weekday == date.today().weekday():
                return OpeningHourSerializer(op_hour).data
            else:
                op_hour = OpeningHourSerializer(op_hour).data
                op_hour["from_hour"] = settings.DEFAULT_OPENING_HOURS[0]["from_hour"]
                op_hour["to_hour"] = settings.DEFAULT_OPENING_HOURS[0]["to_hour"]
                return op_hour


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = (
            "id",
            "payment_provider",
            "name",
            "description",
        )


class PaymentSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "method",
            "orders",
            "amount",
            "currency",
        )


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = (
            "id",
            "rate",
            "name",
            "value",
        )
