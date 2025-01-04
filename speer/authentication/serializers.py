import re
from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class signupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValidationError(
                "Password must contain at least one uppercase letter.")
        if not re.search(r"[0-9]", value):
            raise ValidationError(
                "Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError(
                "Password must contain at least one special character.")
        return value

    def create(self, data):
        data['password'] = make_password(data['password'])
        return super(signupSerializer, self).create(data)
