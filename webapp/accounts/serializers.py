from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=5,
        max_length=20
    )
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]

    def validate(self, attrs):
        if User.objects.filter(
            username=attrs["username"]
        ).exists():
            raise serializers.ValidationError(
                {
                    "username":"Username already exists"
                }
            )
        if User.objects.filter(
            email=attrs["email"]
        ).exists():
            raise serializers.ValidationError(
                {
                    "email":"Email already exists"
                }
            )
        
        validate_password(attrs["password"])

        return attrs
    

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                **validated_data
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {
                    "detail":"Username or email alreay exists"
                }
            )
        
        refresh = RefreshToken.for_user(
            user
        )

        return {
            "user":user,
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

