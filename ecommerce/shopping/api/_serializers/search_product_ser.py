from rest_framework import serializers

from shopping.models import Product


class ValidateSearchQuery(serializers.Serializer):
    query_text = serializers.CharField(
        max_length = 40,
        error_messages = {
            "max_length": "query_text must be of minimum 40 characters",
            "blank": "query_text must not be blank",
            "required": "query_text is required field",
        }
    )


class ProductSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()
    dislike_count = serializers.ReadOnlyField()
    net_likes = serializers.ReadOnlyField()
    in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        exclude = ("recommendation_cluster", )