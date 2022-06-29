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

    def update(self, instance, validated_data):
        if "password" in validated_data.keys():
            instance.set_password(validated_data["password"])
            instance.save()
            del validated_data["password"]

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance


class ChangeActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "is_active",
            "date_joined",
        ]
        read_only_fields = [
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]
