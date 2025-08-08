from rest_framework import serializers

from account.models import UserAddress

# Here instead of making different validation class and all
# I decided to make this serializer and validate here only
# because of simplicity of API

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        exclude = ["created_at", "updated_at", "id"]
    

class CreateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            "pincode", 
            "address_type", 
            "main_address", 
            "city", 
            "state", 
            "country"
        ]
    
    def validate_main_address(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Address must be at least 10 characters long")
        return value.strip()