from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User



class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        read_only=True
    )
    id = serializers.IntegerField(
        read_only=True
    )

    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "bio",
            "phone_number",
            "telegram_id"
        ]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]

    def validate(self, attrs):
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
                    "detail":"Email alreay exists"
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

