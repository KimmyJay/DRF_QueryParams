from rest_framework import serializers

from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = "__all__"
        fields = ["name"]

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Item
        # fields = "__all__"
        fields = ["id", "name", "category", "image_url"]

class OrderSerializer(serializers.ModelSerializer):
    # items = ItemSerializer(many=True, source="item_set", read_only=True)

    class Meta:
        model = Order
        # fields = "__all__"
        fields = ["order_date", "delivery_address"]

class ItemOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    item_name = serializers.ReadOnlyField(source='item.name')

    class Meta:
        model = ItemOrder
        # fields = "__all__"
        fields = ["id", "order", "item", "item_name", "item_count"]
