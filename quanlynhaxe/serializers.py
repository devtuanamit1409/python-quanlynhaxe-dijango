from rest_framework import serializers
from .models import CustomUser, NhaXe, TuyenXe, ChuyenXe, Booking , Delivery, Review
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "role",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    def create(self, validated_data):
        # Tạo một người dùng mới và băm mật khẩu trước khi lưu
        user = CustomUser(
            username=validated_data["username"],
            
            is_active=validated_data.get("is_active", True),
            is_staff=validated_data.get("is_staff", False),
            is_superuser=validated_data.get("is_superuser", False),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class NhaXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhaXe
        fields = "__all__"


class TuyenXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuyenXe
        fields = "__all__"


class ChuyenXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChuyenXe
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
