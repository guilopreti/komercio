from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]
        read_only_fields = ["date_joined"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["email", "password"]
#         extra_kwargs = {"email": {"write_only": True}, "password": {"write_only": True}}
