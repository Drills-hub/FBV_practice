from venv import create
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class Profilerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "username", "email", "nickname", "introduction"
