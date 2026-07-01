from django.contrib.auth.models import AbstractUser
from django.db import models


# class User(AbstractUser):
#     email = models.EmailField(
#         unique=True
#     )
#     avatar = models.ImageField(
#         upload_to='avatars/',
#         null=True,
#         blank=True
#     )
#     bio = models.TextField(
#         max_length=100,
#         blank=True
#     )
#     phone_number = models.CharField(
#         max_length=13,
#         blank=True,
#         null=True
#     )
#     telegram_id = models.CharField(
#         max_length=50,
#         null=True,
#         blank=True
#     )
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = [
#         'username'
#     ]

#     def __str__(self):
#         return self.username