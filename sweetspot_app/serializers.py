from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Customer, Cake, CakeCustomization, Cart, Order,Store

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def validate_mobile_no(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Invalid mobile number. It should be 10 digits.")
        return value

    def create(self, validated_data):
        # Hash the password using make_password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = '__all__'

    def validate_price(self, value):
        try:
            float(value)  # Check if price can be converted to float
        except ValueError:
            raise serializers.ValidationError("Price must be a valid number")
        return value

class CakeCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeCustomization
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def validate_quantity(self, value):
        if not value.isdigit() or int(value) <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        return value

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total_price', 'order_date')  # Calculated fields

    def validate_quantity(self, value):
        if not value.isdigit() or int(value) <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        return value

    def validate_delivery_address(self, value):
        if len(value) > 225:
            raise serializers.ValidationError("Delivery address is too long")
        return value


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
    
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name is too short. It must be at least 3 characters long.")
        if len(value) > 100:
            raise serializers.ValidationError("Name is too long. It must be less than or equal to 100 characters.")
        return value

    def validate_city(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("City name is too short. It must be at least 2 characters long.")
        if len(value) > 100:
            raise serializers.ValidationError("City name is too long. It must be less than or equal to 100 characters.")
        return value

    def validate_contact_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Contact number must contain only digits.")
        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Contact number must be between 10 and 15 digits.")
        return value

    def validate_email(self, value):
        if not serializers.EmailField().run_validation(value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_description(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Description is too long. It must be less than or equal to 500 characters.")
        return value
